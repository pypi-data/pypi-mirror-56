"""Anomaly Detection Example"""
from __future__ import print_function
import os
import sys
import argparse
import math
from collections import Counter
import ipaddress

# Third Party Imports
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans, DBSCAN

# Local imports
from zat import log_to_dataframe, dataframe_to_matrix
from zat.utils import geo_query

# Make some simple data enhancements
def traffic_direction(row):
    # First try to use the local orig/resp fields
    if row.get('local_orig') and row.get('local_resp'):
        local_orig = row['local_orig']
        local_resp = row['local_resp']
    else:
        # Well we don't have local orig/resp fields so use RFC1918 logic
        local_orig = ipaddress.ip_address(row['id.orig_h']).is_private
        local_resp = ipaddress.ip_address(row['id.resp_h']).is_private

    # Determine north/south or internal traffic
    if (not local_orig) and local_resp:
        return 'incoming'
    elif local_orig and not local_resp:
        return 'outgoing'
    else:
        return 'internal'


my_geo = geo_query.GeoQuery()
def country_lookup(row):
    # Get geographical country code
    if row['direction'] == 'internal':
        return 'United States'  # Assume US if internal

    # Greb the 'outside' ip_address
    if row['direction'] == 'incoming':
        ip_address = row['id.orig_h']
    else:
        ip_address = row['id.resp_h']

    # Get the geographical country code
    geo_info = my_geo.query_ip(ip_address)
    if geo_info:
        return geo_info['country_name'] if geo_info['country_name'] else 'Unknown'
    else:
        return 'United States'  # Assume US if we can't find it  


# Setup some pandas options
pd.set_option('display.width', 800)
pd.set_option('max_colwidth', 15)
pd.set_option('max_columns', 10)


# foo += ['country_code']
if __name__ == '__main__':
    # Example to show the dataframe cache functionality on streaming data
    pd.set_option('display.width', 1000)

    # Collect args from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('conn_log', type=str, help='Specify a Zeek conn log to run the explorer on')
    args, commands = parser.parse_known_args()

    # Check for unknown args
    if commands:
        print('Unrecognized args: %s' % commands)
        sys.exit(1)

    # File may have a tilde in it
    if args.conn_log:
        args.conn_log = os.path.expanduser(args.conn_log)

        # Sanity check that this is a conn log
        if 'conn' not in args.conn_log:
            print('This example only works with Zeek with conn.log files..')
            sys.exit(1)

        # Create a Pandas dataframe from a Zeek log
        try:
            log_to_df = log_to_dataframe.LogToDataFrame()
            conn_df = log_to_df.create_dataframe(args.conn_log)
            print(conn_df.head())
        except IOError:
            print('Could not open or parse the specified logfile: %s' % args.conn_log)
            sys.exit(1)
        print('Read in {:d} Rows...'.format(len(conn_df)))
        conn_df.info()

        # Compute the traffic direction
        conn_df['direction'] = conn_df.apply(traffic_direction, axis=1)

        # Filter out internal traffic
        
        # Based on direction lookup geographic country codes
        conn_df['country'] = conn_df.apply(country_lookup, axis=1)
        conn_df = conn_df[~conn_df['country'].isin(['United States', 'Unknown'])]

        # Convert duration to seconds
        conn_df['seconds'] = conn_df['duration'].dt.total_seconds()
        conn_df['seconds'].fillna(0, inplace=True)

        # Features
        features = ['country', 'direction', 'proto', 'service', 'seconds', 'orig_ip_bytes', 'resp_ip_bytes']
        # features = ['country', 'direction', 'proto', 'service', 'seconds']

        # Use the zat DataframeToMatrix class
        to_matrix = dataframe_to_matrix.DataFrameToMatrix()
        conn_matrix = to_matrix.fit_transform(conn_df[features])
        print(conn_matrix.shape)

        # Train/fit and Predict anomalous instances using the Isolation Forest model
        odd_clf = IsolationForest(contamination=0.20, behaviour='new')  # Marking 5% as odd
        odd_clf.fit(conn_matrix)

        # Now we create a new dataframe using the prediction from our classifier
        predictions = odd_clf.predict(conn_matrix)
        odd_df = conn_df[features][predictions == -1]
        display_df = conn_df[predictions == -1]

        # Now we're going to explore our odd observations with help from DBSCAN clustering
        odd_matrix = to_matrix.fit_transform(odd_df)
        display_df['cluster'] = KMeans(n_clusters=5).fit_predict(odd_matrix)
        print(odd_matrix.shape)

        # Group the results by cluster
        cluster_groups = display_df[features+['cluster']].groupby(['cluster'])

        # Now print out the details for each cluster
        print('<<< Outliers Detected! >>>')
        for key, group in cluster_groups:
            print('\nCluster {:d}: {:d} observations'.format(key, len(group)))
            group_matrix = to_matrix.fit_transform(group)
            group['sub_cluster'] = DBSCAN(min_samples=1).fit_predict(group_matrix)
            sub_groups = group[features+['sub_cluster']].groupby(['sub_cluster'])
            for sub_key, sub_group in sub_groups:
                print('\tSub-cluster {:d}: {:d} observations'.format(sub_key, len(sub_group)))
                print(sub_group.head())
