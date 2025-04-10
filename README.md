# http-gateway-mre-20250410

Minimum reproducible example demonstrating a problem I'm having where I can successfully make GET requests to an AWS HTTP API that uses an IAM authorizer, but I cannot make POST requests to same

## Deploy
  

```
sam deploy --parameter-overrides 'pZoneName=my-route53-zone.tld,pHostedZoneId=Z1234567890ABCDEF123'
```

### Parameters

* pHostedZoneId: Route53 hosted zone ID
* pZoneName: Route53 zone name
