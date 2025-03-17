from django_restframework import serializers

from userauths.models import Profile, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = "__all__"  # fields = ('user', 'bio', 'image')
    
    def to_representation(self, instance):
        # instance object to dictionary response
        response = super().to_representation(instance)
        # add additional data to the respose from UserSerializer
        response['user'] = UserSerializer(instance.user).data
        return response
    
