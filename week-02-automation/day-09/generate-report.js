const path = require("path");
const { getRegion, createEc2Client, createS3Client, createRdsClient, createCostExplorerClient } = require("./aws-clients");
const { collectEc2Instances, collectS3Buckets, collectRdsInstances } = require("./resource-collectors");
const { collectServiceCosts } = require("./cost-collector");
const { writeJsonFile, writeCsvFile } = require("./file-helpers");

async function main() {
  const region = getRegion();
  const ec2Client = createEc2Client();
  const s3Client = createS3Client();
  const rdsClient = createRdsClient();
  const ceClient = createCostExplorerClient();

  console.log(`Generating AWS resource report for region ${region}...`);

  const [ec2Instances, s3Buckets, rdsInstances, costs] = await Promise.all([
    collectEc2Instances(ec2Client, region),
    collectS3Buckets(s3Client),
    collectRdsInstances(rdsClient, region),
    collectServiceCosts(ceClient),
  ]);

  const report = {
    generatedAt: new Date().toISOString(),
    region,
    resources: { ec2Instances, s3Buckets, rdsInstances },
    costs,
  };

  const reportsDir = path.join(process.cwd(), "reports");

  // JSON report
  await writeJsonFile(path.join(reportsDir, "aws-resources.json"), report);

  // CSV reports
  if (ec2Instances.length > 0) {
    await writeCsvFile(path.join(reportsDir, "ec2-instances.csv"), ec2Instances);
  }
  if (s3Buckets.length > 0) {
    await writeCsvFile(path.join(reportsDir, "s3-buckets.csv"), s3Buckets);
  }
  if (rdsInstances.length > 0) {
    await writeCsvFile(path.join(reportsDir, "rds-instances.csv"), rdsInstances);
  }

  const costRows = [];
  costRows.push({ service: "EC2", cost: costs.ec2 });
  costRows.push({ service: "S3", cost: costs.s3 });
  costRows.push({ service: "RDS", cost: costs.rds });
  for (const other of costs.otherServices) {
    costRows.push({ service: other.service, cost: other.cost });
  }

  if (costRows.length > 0) {
    await writeCsvFile(path.join(reportsDir, "service-costs.csv"), costRows);
  }

  console.log(`Report generated in ${reportsDir}`);
}

main().catch((err) => {
  console.error("Error generating AWS resource report:", err);
  process.exitCode = 1;
});