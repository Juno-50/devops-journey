const { GetCostAndUsageCommand } = require("@aws-sdk/client-cost-explorer");

function getCurrentMonthPeriod() {
  const now = new Date();
  const start = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), 1));
  const end = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
  const toIsoDate = (d) => d.toISOString().slice(0, 10);
  return { start: toIsoDate(start), end: toIsoDate(end) };
}

async function collectServiceCosts(costExplorerClient) {
  const { start, end } = getCurrentMonthPeriod();
  const cmd = new GetCostAndUsageCommand({
    TimePeriod: { Start: start, End: end },
    Granularity: "MONTHLY",
    Metrics: ["UnblendedCost"],
    GroupBy: [{ Type: "DIMENSION", Key: "SERVICE" }],
  });

  const resp = await costExplorerClient.send(cmd);
  const resultsByTime = resp.ResultsByTime || [];
  const costMap = {};

  for (const result of resultsByTime) {
    const groups = result.Groups || [];
    for (const group of groups) {
      const serviceName = group.Keys && group.Keys[0];
      const amountStr = group.Metrics && group.Metrics.UnblendedCost && group.Metrics.UnblendedCost.Amount;
      if (!serviceName || amountStr == null) continue;
      const amount = parseFloat(amountStr);
      if (!Number.isNaN(amount)) {
        costMap[serviceName] = (costMap[serviceName] || 0) + amount;
      }
    }
  }

  // Normalize into specific services plus all others.
  const lookupNames = {
    ec2: ["Amazon Elastic Compute Cloud - Compute", "Amazon EC2"],
    s3: ["Amazon Simple Storage Service", "Amazon S3"],
    rds: ["Amazon Relational Database Service", "Amazon RDS Service"],
  };

  const normalized = {
    ec2: pickFirstServiceCost(costMap, lookupNames.ec2),
    s3: pickFirstServiceCost(costMap, lookupNames.s3),
    rds: pickFirstServiceCost(costMap, lookupNames.rds),
    otherServices: [],
  };

  for (const [service, cost] of Object.entries(costMap)) {
    if (!lookupNames.ec2.includes(service) &&
        !lookupNames.s3.includes(service) &&
        !lookupNames.rds.includes(service)) {
      normalized.otherServices.push({ service, cost });
    }
  }

  return normalized;
}

function pickFirstServiceCost(costMap, names) {
  for (const name of names) {
    if (Object.prototype.hasOwnProperty.call(costMap, name)) {
      return costMap[name];
    }
  }
  return 0;
}

module.exports = { collectServiceCosts };