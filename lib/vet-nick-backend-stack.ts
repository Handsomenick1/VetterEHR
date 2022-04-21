import { createAppointmentLambda, createPaymentLambda } from './resource/lambda';
import { createTable } from './resource/dynamodb';
import { createTopic } from './resource/sns';
import { CfnOutput, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { createRestAPI } from './resource/apigateway'
import * as apigw from "aws-cdk-lib/aws-apigateway";

export class VetNickBackendStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const APIAppointment = createRestAPI(this, 'Vet-Appointment')
    const APIPayment = createRestAPI(this, 'Vet-Payment')

    new CfnOutput(this, "AppointmentEndpoint", {
      value: APIAppointment.urlForPath("/appointment")
    });
    new CfnOutput(this, "PaymentEndpoint", {
      value: APIAppointment.urlForPath("/payment")
    });

    // DynamoDB table
    const payment_table = createTable(this, 'Vet_payment', 'paymentId');
    const appointment_table = createTable(this, 'Vet_appointment', 'appointmentId')

    const setAppointment_lambda = createAppointmentLambda(this, 'Vet-setAppointment', 'setAppointment.lambda_handler', {
      "region": this.region,
      "payment_table": payment_table.tableName,
      "appointment_table" : appointment_table.tableName

    });
    const getAppointment_lambda = createAppointmentLambda(this, 'Vet-getAppointment', 'getAppointment.lambda_handler', {
      "region": this.region,
      "payment_table": payment_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const cancelAppointment_lambda = createAppointmentLambda(this, 'Vet-cancelAppointment', 'cancelAppointment.lambda_handler', {
      "region": this.region,
      "payment_table": payment_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const confirmAppointment_lambda = createAppointmentLambda(this, 'Vet-confirmAppointment', 'confirmAppointment.lambda_handler', {
      "region": this.region,
      "payment_table": payment_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const createPayment_lambda = createPaymentLambda(this, 'Vet-createPayment', 'createPayment.lambda_handler', {
      "region": this.region,
      "payment_table": payment_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const updatePayment_lambda = createPaymentLambda(this, 'Vet-updatePayment', 'updatePayment.lambda_handler', {
      "region": this.region,
      "payment_table": payment_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const getPayment_lambda = createPaymentLambda(this, 'Vet-getPayment', 'getPayment.lambda_handler', {
      "region": this.region,
      "payment_table": payment_table.tableName,
      "appointment_table" : appointment_table.tableName
    });

    const vet_topic = createTopic(this, 'vet_topic', 'VetTopic','topic-vet')

    const postApmtResource = APIAppointment.root.addResource("appointment", {
      defaultCorsPreflightOptions: {
        allowOrigins: ['*'],
        allowCredentials: true
    },
    defaultMethodOptions: {
      methodResponses: [{
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true 
          }
      }]
    }
    });
    const getApmtResource = APIAppointment.root.addResource("appointmentinfo", {
      defaultCorsPreflightOptions: {
        allowOrigins: ['*'],
        allowCredentials: true
    },
    defaultMethodOptions: {
      methodResponses: [{
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true 
          }
      }]
    }
    });
    const cancelApmtResource = APIAppointment.root.addResource("cancel", {
      defaultCorsPreflightOptions: {
        allowOrigins: ['*'],
        allowCredentials: true
    },
    defaultMethodOptions: {
      methodResponses: [{
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true 
          }
      }]
    }
    });
    const confirmApmtResource = APIAppointment.root.addResource("confirmation", {
      defaultCorsPreflightOptions: {
        allowOrigins: ['*'],
        allowCredentials: true
    },
    defaultMethodOptions: {
      methodResponses: [{
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true 
          }
      }]
    }
    });
    const createPaymentResource = APIPayment.root.addResource("new", {
      defaultCorsPreflightOptions: {
        allowOrigins: ['*'],
        allowCredentials: true
    },
    defaultMethodOptions: {
      methodResponses: [{
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true 
          }
      }]
    }
    });
    const updatePaymentResource = APIPayment.root.addResource("updating", {
      defaultCorsPreflightOptions: {
        allowOrigins: ['*'],
        allowCredentials: true
    },
    defaultMethodOptions: {
      methodResponses: [{
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true 
          }
      }]
    }
    });
    const getPaymentResource = APIPayment.root.addResource("paymentinfo", {
      defaultCorsPreflightOptions: {
        allowOrigins: ['*'],
        allowCredentials: true
    },
    defaultMethodOptions: {
      methodResponses: [{
          statusCode: "200",
          responseParameters: {
            'method.response.header.Content-Type': true 
          }
      }]
    }
    });

    postApmtResource.addMethod(
      'POST',
      new apigw.LambdaIntegration(setAppointment_lambda, {proxy: false, 
        integrationResponses: [
        {statusCode: "200"}
        ]}),
      {
        methodResponses: [
          {
            statusCode: "200",
            responseParameters: {
              "method.response.header.Access-Control-Allow-Methods": true,
              "method.response.header.Access-Control-Allow-Headers": true,
              "method.response.header.Access-Control-Allow-Origin": true
            }
          }
        ]
      });

    getApmtResource.addMethod(
      'GET',
      new apigw.LambdaIntegration(getAppointment_lambda)
    )
    cancelApmtResource.addMethod(
      'PATCH',
      new apigw.LambdaIntegration(cancelAppointment_lambda, {proxy: false, 
        integrationResponses: [
        {statusCode: "200"}
        ]}),
      {
        methodResponses: [
          {
            statusCode: "200",
            responseParameters: {
              "method.response.header.Access-Control-Allow-Methods": true,
              "method.response.header.Access-Control-Allow-Headers": true,
              "method.response.header.Access-Control-Allow-Origin": true
            }
          }
        ]
      });
    confirmApmtResource.addMethod(
      'PATCH',
      new apigw.LambdaIntegration(confirmAppointment_lambda, {proxy: false, 
        integrationResponses: [
        {statusCode: "200"}
        ]}),
      {
        methodResponses: [
          {
            statusCode: "200",
            responseParameters: {
              "method.response.header.Access-Control-Allow-Methods": true,
              "method.response.header.Access-Control-Allow-Headers": true,
              "method.response.header.Access-Control-Allow-Origin": true
            }
          }
        ]
      });
    createPaymentResource.addMethod(
      'POST',
      new apigw.LambdaIntegration(createPayment_lambda, {proxy: false, 
        integrationResponses: [
        {statusCode: "200"}
        ]}),
      {
        methodResponses: [
          {
            statusCode: "200",
            responseParameters: {
              "method.response.header.Access-Control-Allow-Methods": true,
              "method.response.header.Access-Control-Allow-Headers": true,
              "method.response.header.Access-Control-Allow-Origin": true
            }
          }
        ]
      });

    updatePaymentResource.addMethod(
      'PATCH',
      new apigw.LambdaIntegration(updatePayment_lambda, {proxy: false, 
        integrationResponses: [
        {statusCode: "200"}
        ]}),
      {
        methodResponses: [
          {
            statusCode: "200",
            responseParameters: {
              "method.response.header.Access-Control-Allow-Methods": true,
              "method.response.header.Access-Control-Allow-Headers": true,
              "method.response.header.Access-Control-Allow-Origin": true
            }
          }
        ]
      });
    getPaymentResource.addMethod(
      'GET',
      new apigw.LambdaIntegration(updatePayment_lambda)
    )
    payment_table.grantFullAccess(createPayment_lambda);
    payment_table.grantFullAccess(updatePayment_lambda);
    payment_table.grantFullAccess(getPayment_lambda);

    appointment_table.grantFullAccess(setAppointment_lambda);
    appointment_table.grantFullAccess(getAppointment_lambda);
    appointment_table.grantFullAccess(cancelAppointment_lambda);
    appointment_table.grantFullAccess(confirmAppointment_lambda);

    vet_topic.grantPublish(cancelAppointment_lambda);
    vet_topic.grantPublish(confirmAppointment_lambda);
    vet_topic.grantPublish(updatePayment_lambda);
    vet_topic.grantPublish(updatePayment_lambda);
    
  }
}
