import * as lambda from 'aws-cdk-lib/aws-lambda'
import { Stack } from 'aws-cdk-lib'
import * as path from 'path'

export function createAppointmentLambda(stack: Stack, funcName: string, handlerPath: string, environVars: {}): lambda.Function{
    let lambdaFunction = new lambda.Function(stack, funcName, {
        runtime:lambda.Runtime.PYTHON_3_9,
        functionName: funcName,
        code: lambda.Code.fromAsset(path.join(__dirname, `../lambdafunctions/appointment`)),
        handler: handlerPath,
        environment: environVars,
        memorySize: 512
    });

    return lambdaFunction;
}

export function createPaymentLambda(stack: Stack, funcName: string, handlerPath: string, layersName1: string, environVars: {}): lambda.Function{
    let lambdaFunction = new lambda.Function(stack, funcName, {
        runtime:lambda.Runtime.PYTHON_3_9,
        functionName: funcName,
        code: lambda.Code.fromAsset(path.join(__dirname, `../lambdafunctions/payment`)),
        handler: handlerPath,
        environment: environVars,
        memorySize: 512,
        layers: [lambda.LayerVersion.fromLayerVersionAttributes(stack, layersName1, {
            layerVersionArn: "arn:aws:lambda:us-west-2:568187732893:layer:strip:1",
            compatibleRuntimes: [ lambda.Runtime.PYTHON_3_9, lambda.Runtime.PYTHON_3_8]
        }), 
        ]
    });

    return lambdaFunction;
}