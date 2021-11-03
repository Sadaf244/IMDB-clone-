from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform,Review
 
class ReviewSerializer(serializers.ModelSerializer):
    reviewer=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        #fields="__all__"
        exclude=('watchlist',)


class WatchListSerializer(serializers.ModelSerializer):
    #reviews=ReviewSerializer(many=True,read_only=True)
    #len_name=serializers.SerializerMethodField()
    platform=serializers.CharField(source='platform.name')
    class Meta:
        model=WatchList
        fields="__all__"
        #fields=['id',name','description']
        #exclude=['active']
    #def get_len_name(self , object):
        #return len(object.title)


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist=WatchListSerializer(many=True,read_only=True) # one Streaming Platform has many watchlist platform
    #watchlist=serializers.StringRelatedField(many=True)#StringRelatedField may be used to represent the target of the relationship using its __str__ method.
    #watchlist=serializers.HyperlinkedRelatedField(
      #  many=True,
        #read_only=True,
       # view_name='movie-details'
    #)
    #HyperlinkedRelatedField may be used to represent the target of the relationship using a hyperlink.
   
    class Meta:
        model=StreamPlatform
        fields="__all__"

    

    #def validate_name(self,value): #Field Level Validation
    #    if len(value)<2:
    #        raise serializers.ValidationError("The name is too short.")
    #    else:
    #        return value

    #def validate(self,data):  #Object Level Validation
    #    if data['title']==data['storyline']:
    #        raise serializers.ValidationError("title and Storyline should not be same")
    #    else:
    #        return data

#def name_length(value): #Validators
#    if len(value)<2:
 #           raise serializers.ValidationError("The name is too short.")

#class MovieSerializer(serializers.Serializer):
#    id=serializers.IntegerField(read_only=True)
 #   name=serializers.CharField(validators=[name_length])
 #   description=serializers.CharField()
 #   active=serializers.BooleanField(default=False)
    
    #def create(self,validated_data):
    #    return Movie.objects.create(**validated_data)

    #def update(self,instance,validated_data):
    #    instance.name=validated_data.get('name',instance.name)
    #    instance.description=validated_data.get('description',instance.description)
    #    instance.active=validated_data.get('active',instance.active)
    #    instance.save()
    #   return instance
 
    

    #def validate_name(self,value): #Field Level Validation
       # if len(value)<2:
         #   raise serializers.ValidationError("The name is too short.")
       # else:
       #     return value
        
