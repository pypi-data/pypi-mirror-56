## Amazon DynamoDB Construct Library

<html></html>---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<html></html>

Here is a minimal deployable DynamoDB table definition:

```python
# Example may have issues. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_dynamodb as dynamodb

table = dynamodb.Table(self, "Table",
    partition_key=Attribute(name="id", type=dynamodb.AttributeType.STRING)
)
```

### Keys

When a table is defined, you must define it's schema using the `partitionKey`
(required) and `sortKey` (optional) properties.

### Billing Mode

DynamoDB supports two billing modes:

* PROVISIONED - the default mode where the table and global secondary indexes have configured read and write capacity.
* PAY_PER_REQUEST - on-demand pricing and scaling. You only pay for what you use and there is no read and write capacity for the table or its global secondary indexes.

```python
# Example may have issues. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_dynamodb as dynamodb

table = dynamodb.Table(self, "Table",
    partition_key=Attribute(name="id", type=dynamodb.AttributeType.STRING),
    billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
)
```

Further reading:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.

### Configure AutoScaling for your table

You can have DynamoDB automatically raise and lower the read and write capacities
of your table by setting up autoscaling. You can use this to either keep your
tables at a desired utilization level, or by scaling up and down at preconfigured
times of the day:

Auto-scaling is only relevant for tables with the billing mode, PROVISIONED.

```ts lit=test/integ.autoscaling.lit.ts
const readScaling = table.autoScaleReadCapacity({ minCapacity: 1, maxCapacity: 50 });

readScaling.scaleOnUtilization({
  targetUtilizationPercent: 50
});

readScaling.scaleOnSchedule('ScaleUpInTheMorning', {
  schedule: appscaling.Schedule.cron({ hour: '8', minute: '0' }),
  minCapacity: 20,
});

readScaling.scaleOnSchedule('ScaleDownAtNight', {
  schedule: appscaling.Schedule.cron({ hour: '20', minute: '0' }),
  maxCapacity: 20
});
```

Further reading:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html
https://aws.amazon.com/blogs/database/how-to-use-aws-cloudformation-to-configure-auto-scaling-for-amazon-dynamodb-tables-and-indexes/

### Amazon DynamoDB Global Tables

Please see the `@aws-cdk/aws-dynamodb-global` package.
