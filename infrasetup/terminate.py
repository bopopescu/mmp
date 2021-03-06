#!/usr/bin/env python
import sys
import boto3
import time

#reg = input("Enter the region:")

#ec2 = boto3.resource('ec2', region_name = reg)
#client = boto3.client('ec2', region_name = reg)
#elb = boto3.client('elb', region_name = reg)
#autoscaling = boto3.client('autoscaling', region_name = reg)

#MasterASG = input("Enter MasterASG name:")
#SlaveASG = input("Enter SlaveASG name:")

def cluster_termination(reg,ec2,client,elb,autoscaling,MasterASG,SlaveASG):

	describeinstances = autoscaling.describe_auto_scaling_instances()
	length = len(describeinstances['AutoScalingInstances'])
	instanceid = []
	for i in range(0,length):
	        instanceid.append(describeinstances['AutoScalingInstances'][i]['InstanceId'])
	print instanceid

	updateautoscalinggroupmaster = autoscaling.update_auto_scaling_group(
	        AutoScalingGroupName = MasterASG,
	        MinSize = 0,
	        DesiredCapacity = 0,)

	updateautoscalinggroupslave = autoscaling.update_auto_scaling_group(
                AutoScalingGroupName = SlaveASG,
                MinSize = 0,
                DesiredCapacity = 0,)

	print updateautoscalinggroupmaster
	print updateautoscalinggroupslave

#detachinstances = autoscaling.detach_instances(
#               InstanceIds = instanceid,
#               AutoScalingGroupName = 'my-auto-scaling-group',
#               ShouldDecrementDesiredCapacity = True)



	Loadbalancerdeletemaster = elb.delete_load_balancer(
	        LoadBalancerName = MasterASG)

	Loadbalancerdeleteslave = elb.delete_load_balancer(
                LoadBalancerName = SlaveASG)

	print Loadbalancerdeletemaster
	print Loadbalancerdeleteslave


	time.sleep(200)


	Autoscalinggroupdeletemaster = autoscaling.delete_auto_scaling_group(
	        AutoScalingGroupName = MasterASG)
	Autoscalinggroupdeleteslave = autoscaling.delete_auto_scaling_group(
                AutoScalingGroupName = SlaveASG)

	print Autoscalinggroupdeletemaster
	print Autoscalinggroupdeleteslave

	
	
	Launchconfigurationdeletemaster = autoscaling.delete_launch_configuration(
	        LaunchConfigurationName = MasterASG)
	Launchconfigurationdeleteslave = autoscaling.delete_launch_configuration(
                LaunchConfigurationName = SlaveASG)

	#print Launchconfigurationdeletemaster
	#print Launchconfigurationdeleteslave

#for i in range(0,length):
#       instances = ec2.Instance(instanceid[i])
#       response = instance.terminate()
#       print response
#       instance.wait_until_terminated()

	#vpc =  list(ec2.vpcs.filter(Filters=[{'Name':'tag:Name','Values':['test_vpc']}]))

	#sec_group = list(vpc[0].security_groups.all())
	#for i in sec_group:
	 #       if i.group_name != 'default':
	  #              response = i.delete()
	   #             print response

	#ig = list(vpc[0].internet_gateways.all())
	#for i in ig:
	 #       i.detach_from_vpc(VpcId = vpc[0].vpc_id)
	  #      response = i.delete()
	   #     print response

	#subnets = list(vpc[0].subnets.all())
	#for i in subnets:
	 #       response = i.delete()
	  #      print response

	#route_table = list(vpc[0].route_tables.filter(Filters = [{'Name':'tag:Name','Values':['routetable']}]))
	#for i in route_table:
	 #       response = i.delete()
	  #      print response

	#response = vpc[0].delete()
	#print response

#terminate = cluster_termination(reg,ec2,client,elb,autoscaling,MasterASG,SlaveASG)