const {
  DescribeInstancesCommand,
  paginateDescribeInstances,
} = require("@aws-sdk/client-ec2");
const {
  ListBucketsCommand,
  GetBucketLocationCommand,
} = require("@aws-sdk/client-s3");
const {
  DescribeDBInstancesCommand,
  paginateDescribeDBInstances,
} = require("@aws-sdk/client-rds");

// EC2: list all instances in the configured region
async function collectEc2Instances(ec2Client, region) {
  const instances = [];
  const paginator = paginateDescribeInstances({ client: ec2Client }, {});
  for await (const page of paginator) {
    const reservations = page.Reservations || [];
    for (const reservation of reservations) {
      const resInstances = reservation.Instances || [];
      for (const instance of resInstances) {
        instances.push({
          instanceId: instance.InstanceId,
          instanceType: instance.InstanceType,
          state: instance.State ? instance.State.Name : undefined,
          availabilityZone: instance.Placement ? instance.Placement.AvailabilityZone : undefined,
          region,
          launchTime: instance.LaunchTime ? instance.LaunchTime.toISOString() : undefined,
          tags: normalizeTags(instance.Tags),
        });
      }
    }
  }
  return instances;
}

// S3: list all buckets and annotate with region
async function collectS3Buckets(s3Client) {
  const buckets = [];
  const listResp = await s3Client.send(new ListBucketsCommand({}));
  const bucketList = listResp.Buckets || [];
  for (const bucket of bucketList) {
    const name = bucket.Name;
    let region;
    try {
      const locResp = await s3Client.send(
        new GetBucketLocationCommand({ Bucket: name })
      );
      const loc = locResp.LocationConstraint;
      // us-east-1 is represented as null or empty.
      region = !loc || loc === "" ? "us-east-1" : loc;
    } catch (err) {
      region = "unknown";
    }
    buckets.push({
      name,
      creationDate: bucket.CreationDate ? bucket.CreationDate.toISOString() : undefined,
      region,
    });
  }
  return buckets;
}

// RDS: list all DB instances in the configured region
async function collectRdsInstances(rdsClient, region) {
  const dbInstances = [];
  const paginator = paginateDescribeDBInstances({ client: rdsClient }, {});
  for await (const page of paginator) {
    const instances = page.DBInstances || [];
    for (const db of instances) {
      dbInstances.push({
        dbInstanceIdentifier: db.DBInstanceIdentifier,
        engine: db.Engine,
        engineVersion: db.EngineVersion,
        dbInstanceClass: db.DBInstanceClass,
        status: db.DBInstanceStatus,
        region,
        endpoint: db.Endpoint ? db.Endpoint.Address : undefined,
        allocatedStorage: db.AllocatedStorage,
        multiAz: db.MultiAZ,
        tags: normalizeTags(db.TagList),
      });
    }
  }
  return dbInstances;
}

function normalizeTags(rawTags) {
  if (!rawTags || !Array.isArray(rawTags)) return {};
  const result = {};
  for (const tag of rawTags) {
    if (tag.Key) {
      result[tag.Key] = tag.Value || "";
    }
  }
  return result;
}

module.exports = {
  collectEc2Instances,
  collectS3Buckets,
  collectRdsInstances,
};