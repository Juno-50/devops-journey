#!/usr/bin/env python3
"""
EC2 Instance Controller
Start, stop, or restart EC2 instances by tag
Usage: python ec2_controller.py start --tag Environment=Test
Author: Juno-50 | Day 8 - AWS Learning Journey
"""

import boto3
import argparse
from datetime import datetime

class EC2Controller:
    """EC2 Instance Controller"""
    
    def __init__(self, region='us-east-1'):
        """Initialize EC2 client."""
        self.ec2 = boto3.client('ec2', region_name=region)
        self.region = region
        print(f"✅ Connected to EC2 in region: {region}\n")
    
    def find_instances_by_tag(self, tag_key, tag_value):
        """Find instances matching a tag."""
        print(f"🔍 Searching for instances with tag '{tag_key}={tag_value}'...")
        
        response = self.ec2.describe_instances(
            Filters=[{'Name': f'tag:{tag_key}', 'Values': [tag_value]}]
        )
        
        instance_ids = []
        instance_details = []
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])
                
                # Get instance name
                name = 'No Name'
                if instance.get('Tags'):
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            name = tag['Value']
                
                instance_details.append({
                    'InstanceId': instance['InstanceId'],
                    'Name': name,
                    'State': instance['State']['Name'],
                    'Type': instance['InstanceType']
                })
        
        # Display found instances
        if instance_details:
            print(f"\n  Found {len(instance_details)} instance(s):")
            print(f"{'Instance ID':<20} {'Name':<25} {'State':<15} {'Type':<15}")
            print("-" * 80)
            for inst in instance_details:
                print(f"{inst['InstanceId']:<20} {inst['Name']:<25} {inst['State']:<15} {inst['Type']:<15}")
            print()
        else:
            print(f"⚠️  No instances found with tag '{tag_key}={tag_value}'")
        
        return instance_ids
    
    def start_instances(self, instance_ids, dry_run=False):
        """Start EC2 instances."""
        if not instance_ids:
            print("No instances to start")
            return False
        
        try:
            if dry_run:
                print(f"🔍 DRY RUN: Would start {len(instance_ids)} instance(s)")
                return True
            
            print(f"▶️  Starting {len(instance_ids)} instance(s)...")
            self.ec2.start_instances(InstanceIds=instance_ids)
            
            # Wait for instances to start
            print("Waiting for instances to start...", end="")
            waiter = self.ec2.get_waiter('instance_running')
            waiter.wait(InstanceIds=instance_ids)
            print(" Done!")
            
            print(f"✅ Successfully started {len(instance_ids)} instance(s)")
            return True
        except Exception as e:
            print(f"❌ Error starting instances: {e}")
            return False
    
    def stop_instances(self, instance_ids, dry_run=False):
        """Stop EC2 instances."""
        if not instance_ids:
            print("No instances to stop")
            return False
        
        try:
            if dry_run:
                print(f"🔍 DRY RUN: Would stop {len(instance_ids)} instance(s)")
                return True
            
            print(f"⏸️  Stopping {len(instance_ids)} instance(s)...")
            self.ec2.stop_instances(InstanceIds=instance_ids)
            
            # Wait for instances to stop
            print("Waiting for instances to stop...", end="")
            waiter = self.ec2.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=instance_ids)
            print(" Done!")
            
            print(f"✅ Successfully stopped {len(instance_ids)} instance(s)")
            return True
        except Exception as e:
            print(f"❌ Error stopping instances: {e}")
            return False
    
    def restart_instances(self, instance_ids, dry_run=False):
        """Restart EC2 instances."""
        if not instance_ids:
            print("No instances to restart")
            return False
        
        try:
            if dry_run:
                print(f"🔍 DRY RUN: Would restart {len(instance_ids)} instance(s)")
                return True
            
            print(f"🔄 Restarting {len(instance_ids)} instance(s)...")
            self.ec2.reboot_instances(InstanceIds=instance_ids)
            
            print(f"✅ Successfully restarted {len(instance_ids)} instance(s)")
            return True
        except Exception as e:
            print(f"❌ Error restarting instances: {e}")
            return False

def parse_tag(tag_string):
    """Parse tag string in format 'Key=Value'."""
    try:
        key, value = tag_string.split('=', 1)
        return key.strip(), value.strip()
    except:
        print(f"❌ Invalid tag format: '{tag_string}'. Use 'Key=Value'")
        return None, None

def main():
    """Main function - parse arguments and execute action."""
    parser = argparse.ArgumentParser(
        description='Control EC2 instances by tag',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  python ec2_controller.py start --tag Environment=Dev
  python ec2_controller.py stop --tag Name=test-server
  python ec2_controller.py restart --tag Project=MyApp --dry-run'''
    )
    
    parser.add_argument('action', choices=['start', 'stop', 'restart'], help='Action to perform')
    parser.add_argument('--tag', required=True, help='Tag to filter instances (format: Key=Value)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without executing')
    parser.add_argument('--region', default='us-east-1', help='AWS region (default: us-east-1)')
    
    args = parser.parse_args()
    
    # Print header
    print("=" * 80)
    print(f"EC2 Instance Controller - {args.action.upper()}")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    print()
    
    # Parse tag
    tag_key, tag_value = parse_tag(args.tag)
    if not tag_key:
        return
    
    # Initialize controller
    controller = EC2Controller(region=args.region)
    
    # Find instances
    instance_ids
