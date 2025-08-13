import boto3

def compare_faces(sourceFile, targetFile):
    
    result = ""

    client = boto3.client('rekognition')
    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')
    response = client.compare_faces(SimilarityThreshold=0,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})
    
    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = faceMatch['Similarity']
        result = f"동일 인물일 확률 : {similarity:.2f}%"
        result += "<br/>"
        
    imageSource.close()
    imageTarget.close()
    return result

def main():
    source_file = 'seol.jpg'
    target_file = 'white.jpg'
    face_matches = compare_faces(source_file, target_file)
    print("Face matches: " + str(face_matches))
if __name__ == "__main__":

    main()


def detect_labels_local_file(photo):
    client=boto3.client('rekognition')
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})

    result =[]
    for label in response['Labels']:

        Name = label["Name"]
        Confidence = label["Confidence"]

        result.append(f"{Name}일 확률은 {Confidence:.2f}%")

    return "<br/>".join(map(str, result))