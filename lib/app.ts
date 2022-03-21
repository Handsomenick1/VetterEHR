import { App }from "aws-cdk-lib";
import { VetNickBackendStack } from '../lib/vet-nick-backend-stack'

const app = new App();

new VetNickBackendStack(app, 'cdk-stack-dev', {
    stackName: 'cdk-stack-dev',
    env: {
      account: process.env.CDK_DEFAULT_ACCOUNT,
      region: process.env.CDK_DEFAULT_REGION,
    },
  });
  
// new VetNickBackendStack(app, 'cdk-stack-prod', {
// stackName: 'cdk-stack-prod',
// env: {
//     account: process.env.CDK_DEFAULT_ACCOUNT,
//     region: process.env.CDK_DEFAULT_REGION,
// },
// });
