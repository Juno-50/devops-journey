#!/usr/bin/env python3
"""
EC2 Instance Reporter
Lists all EC2 instances with key details and exports to CSV
Author: Juno-50 | Day 8 - AWS Learning Journey
"""

import boto3
import csv
from datetime import datetime

def get_instance_name(instance):
    """Extract instance name from tags."""
    if instance.get('Tags'):
        for tag in instance['Tags']:
            if tag['Key'] == 'Name':
                return tag['Value']
    return 'No Name'

def list_ec2_instances():
    """List all EC2 instances in the account."""
    print("Connecting to AWS EC2...")
    ec2 = boto3.client('ec2', region_name='us-east-1')
    print("Fetching instances...\n")
    
    response = ec2.describe_instances()
    instances_data = []
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_info = {
                'InstanceId': instance['InstanceId'],
                'Name': get_instance_name(instance),
                'State': instance['State']['Name'],
                'InstanceType': instance['InstanceType'],
                'PublicIP': instance.get('PublicIpAddress', 'N/A'),
                'PrivateIP': instance.get('PrivateIpAddress', 'N/A'),
                'LaunchTime': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S')
            }
            instances_data.append(instance_info)
    
    return instances_data

def print_instances_table(instances):
    """Print instances in formatted table."""
    if not instances:
        print("No EC2 instances found.")
        return
    
    print(f"{'Name':<20} {'Instance ID':<20} {'State':<15} {'Type':<15} {'Public IP':<15}")
    print("-" * 90)
    
    for inst in instances:
        print(f"{inst['Name']:<20} {inst['InstanceId']:<20} {inst['State']:<15} "
              f"{inst['InstanceType']:<15} {inst['PublicIP']:<15}")

def export_to_csv(instances, filename='ec2_instances.csv'):
    """Export instances to CSV file."""
    if not instances:
        print("No data to export.")
        return
    
    fieldnames = ['Name', 'InstanceId', 'State', 'InstanceType', 'PublicIP', 'PrivateIP', 'LaunchTime']
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for instance in instances:
            writer.writerow(instance)
    
    print(f"\n✅ Data exported to {filename}")

def main():
    """Main function."""
    print("=" * 90)
    print("EC2 Instance Reporter")
    print("=" * 90)
    
    try:
        instances = list_ec2_instances()
        print(f"\nFound {len(instances)} instance(s)\n")
        print_instances_table(instances)
        export_to_csv(instances)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure AWS credentials are configured.")

if __name__ == "__main__":
    main()