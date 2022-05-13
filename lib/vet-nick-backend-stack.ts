import { createAppointmentLambda, createPaymentLambda } from './resource/lambda';
import { createTable } from './resource/dynamodb';
import { createTopic } from './resource/sns';
import { CfnOutput, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { createRestAPI } from './resource/apigateway';
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
    const order_table = createTable(this, 'Vet_payment', 'orderId');
    const appointment_table = createTable(this, 'Vet_appointment', 'appointmentId')

    // lambda    
    const setAppointment_lambda = createAppointmentLambda(this, 'Vet-setAppointment', 'setAppointment.lambda_handler', 'jwt1',{
      "region": this.region,
      "order_table": order_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const getAppointment_lambda = createAppointmentLambda(this, 'Vet-getAppointment', 'getAppointment.lambda_handler', 'jwt2', {
      "region": this.region,
      "order_table": order_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const getAllAppointment_lambda = createAppointmentLambda(this, 'Vet-getAllAppointment', 'getAllAppointment.lambda_handler', 'jwt3',{
      "region": this.region,
      "order_table": order_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const cancelAppointment_lambda = createAppointmentLambda(this, 'Vet-cancelAppointment', 'cancelAppointment.lambda_handler', 'jwt4',{
      "region": this.region,
      "order_table": order_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const confirmAppointment_lambda = createAppointmentLambda(this, 'Vet-confirmAppointment', 'confirmAppointment.lambda_handler', 'jwt5',{
      "region": this.region,
      "order_table": order_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const updateAppointment_lambda = createAppointmentLambda(this, 'Vet-updateAppointment', 'updateAppointment.lambda_handler', 'jwt6',{
      "region": this.region,
      "order_table": order_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const getzoomlink_lambda = createAppointmentLambda(this, 'Vet-getZoomlink', 'zoomlink.lambda_handler', 'jwt7',{
      "region": this.region,
      "order_table": order_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const createPayment_lambda = createPaymentLambda(this, 'Vet-createPayment', 'createPayment.lambda_handler', "stripeLayer1", {
      "region": this.region,
      "order_table": order_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const updatePayment_lambda = createPaymentLambda(this, 'Vet-updatePayment', 'updatePayment.lambda_handler', "stripeLayer2", {
      "region": this.region,
      "order_table": order_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const getPayment_lambda = createPaymentLambda(this, 'Vet-getPayment', 'getPayment.lambda_handler', "stripeLayer3",{
      "region": this.region,
      "order_table": order_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    const getallpayment_lambda = createPaymentLambda(this, 'Vet-getAllPayment', 'getAllpayment.lambda_handler', "stripeLayer4",{
      "region": this.region,
      "order_table": order_table.tableName,
      "appointment_table" : appointment_table.tableName
    });
    
    
    // Topic
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
    const getallAptResource = APIAppointment.root.addResource("allappointment", {
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
    const updateApmtResource = APIAppointment.root.addResource("update", {
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

    const zoomlinkResource = APIAppointment.root.addResource("zoomlink", {
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
    const getAllPaymentResource = APIPayment.root.addResource("allpaymentinfo", {
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
    getAllPaymentResource.addMethod(
      "GET",
      new apigw.LambdaIntegration(getallpayment_lambda)
    );
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
    getallAptResource.addMethod(
      'GET',
      new apigw.LambdaIntegration(getAllAppointment_lambda)
    )
    zoomlinkResource.addMethod(
      'POST',
      new apigw.LambdaIntegration(getzoomlink_lambda, {proxy: false, 
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
    updateApmtResource.addMethod(
      'PATCH',
      new apigw.LambdaIntegration(updateAppointment_lambda, {proxy: false, 
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
      'POST',
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
      new apigw.LambdaIntegration(getPayment_lambda)
    )
    
    order_table.grantFullAccess(createPayment_lambda);
    order_table.grantFullAccess(updatePayment_lambda);
    order_table.grantFullAccess(getPayment_lambda);
    order_table.grantFullAccess(getallpayment_lambda);

    appointment_table.grantFullAccess(setAppointment_lambda);
    appointment_table.grantFullAccess(getAppointment_lambda);
    appointment_table.grantFullAccess(cancelAppointment_lambda);
    appointment_table.grantFullAccess(confirmAppointment_lambda);
    appointment_table.grantFullAccess(getAllAppointment_lambda);
    appointment_table.grantFullAccess(updateAppointment_lambda);

    vet_topic.grantPublish(cancelAppointment_lambda);
    vet_topic.grantPublish(confirmAppointment_lambda);
    vet_topic.grantPublish(updatePayment_lambda);
    vet_topic.grantPublish(updatePayment_lambda);
    
  }
}
