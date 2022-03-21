import * as sns from 'aws-cdk-lib/aws-sns';
import { Stack } from 'aws-cdk-lib';

export function createTopic(stack: Stack, id: string, displayName: string, topicName: string): sns.Topic {
    const topic = new sns.Topic(stack, id, {
        displayName: displayName,
        topicName: topicName
    })
    return topic
}