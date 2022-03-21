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

    const setAppointment_lambda = createAppointmentLambda(this, 'setAppointment', 'setAppointment.lambda_handler', {
      "region": this.region
    });
    const getAppointment_lambda = createAppointmentLambda(this, 'getAppointment', 'getAppointment.lambda_handler', {
      "region": this.region
    });
    const cancelAppointment_lambda = createAppointmentLambda(this, 'cancelAppointment', 'cancelAppointment.lambda_handler', {
      "region": this.region
    });
    const confirmAppointment_lambda = createAppointmentLambda(this, 'confirmAppointment', 'confirmAppointment.lambda_handler', {
      "region": this.region
    });
    const createPayment_lambda = createPaymentLambda(this, 'createPayment', 'createPayment.lambda_handler', {
      "region": this.region
    });
    const updatePayment_lambda = createPaymentLambda(this, 'updatePayment', 'updatePayment.lambda_handler', {
      "region": this.region
    });
    const getPayment_lambda = createPaymentLambda(this, 'getPayment', 'getPayment.lambda_handler', {
      "region": this.region
    });
    
    const payment_table = createTable(this, 'payment', 'paymentId');
    const Appointment_table = createTable(this, 'AppointmentTable', 'AppointmentTableId')

    const vet_topic = createTopic(this, 'vet_topic', 'VetTopic','topic-vet')

    const postApmtResource = APIAppointment.root.addResource("setting");
    const getApmtResource = APIAppointment.root.addResource("getting");
    const cancelApmtResource = APIAppointment.root.addResource("cancel");
    const confirmApmtResource = APIAppointment.root.addResource("confirmation");
    const createPaymentResource = APIPayment.root.addResource("new");
    const updatePaymentResource = APIPayment.root.addResource("updating");
    const getPaymentResource = APIPayment.root.addResource("getting");

    postApmtResource.addMethod(
      'POST',
      new apigw.LambdaIntegration(setAppointment_lambda)
    )
    getApmtResource.addMethod(
      'GET',
      new apigw.LambdaIntegration(getAppointment_lambda)
    )
    cancelApmtResource.addMethod(
      'PATCH',
      new apigw.LambdaIntegration(cancelAppointment_lambda)
    )
    confirmApmtResource.addMethod(
      'PATCH',
      new apigw.LambdaIntegration(confirmAppointment_lambda)
    )
    createPaymentResource.addMethod(
      'POST',
      new apigw.LambdaIntegration(createPayment_lambda)
    )
    updatePaymentResource.addMethod(
      'PATCH',
      new apigw.LambdaIntegration(updatePayment_lambda)
    )
    getPaymentResource.addMethod(
      'GET',
      new apigw.LambdaIntegration(updatePayment_lambda)
    )
    payment_table.grantFullAccess(createPayment_lambda);
    payment_table.grantFullAccess(updatePayment_lambda);
    payment_table.grantFullAccess(getPayment_lambda);

    Appointment_table.grantFullAccess(setAppointment_lambda);
    Appointment_table.grantFullAccess(getAppointment_lambda);
    Appointment_table.grantFullAccess(cancelAppointment_lambda);
    Appointment_table.grantFullAccess(confirmAppointment_lambda);

    vet_topic.grantPublish(cancelAppointment_lambda);
    vet_topic.grantPublish(confirmAppointment_lambda);
    vet_topic.grantPublish(updatePayment_lambda);
    vet_topic.grantPublish(updatePayment_lambda);
    
  }
}
