const { EC2Client } = require("@aws-sdk/client-ec2");
const { S3Client } = require("@aws-sdk/client-s3");
const { RDSClient } = require("@aws-sdk/client-rds");
const { CostExplorerClient } = require("@aws-sdk/client-cost-explorer");

function getRegion() {
  // Prefer explicit override for the lab, then fall back to AWS defaults.
  return process.env.REPORT_REGION || process.env.AWS_REGION || process.env.AWS_DEFAULT_REGION || "us-east-1";
}

function createEc2Client() {
  return new EC2Client({ region: getRegion() });
}

function createS3Client() {
  // S3 is global but many APIs still require a region; use same region for consistency.
  return new S3Client({ region: getRegion() });
}

function createRdsClient() {
  return new RDSClient({ region: getRegion() });
}

function createCostExplorerClient() {
  // Cost Explorer is only available in us-east-1.
  return new CostExplorerClient({ region: "us-east-1" });
}

module.exports = {
  getRegion,
  createEc2Client,
  createS3Client,
  createRdsClient,
  createCostExplorerClient,
};