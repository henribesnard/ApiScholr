from rest_framework import serializers
from .models import Post, PostChannel, PostAttachment

class PostChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostChannel
        fields = ['channel_type', 'object_id']

class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ['file']

class PostSerializer(serializers.ModelSerializer):
    channels = PostChannelSerializer(many=True)
    attachments = PostAttachmentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['author', 'channels', 'title', 'text', 'description', 'attachments']

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments')
        channels_data = validated_data.pop('channels')
        post = Post.objects.create(**validated_data)
        for attachment_data in attachments_data:
            PostAttachment.objects.create(post=post, **attachment_data)
        for channel_data in channels_data:
            PostChannel.objects.create(post=post, **channel_data)
        return post
