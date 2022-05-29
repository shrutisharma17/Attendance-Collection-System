from django.shortcuts import render, HttpResponse, redirect
from .models import *
import os
import numpy as np
import face_recognition
import cv2
from .forms import *
from django.db.models import Q



last_face = 'no_face'
current_path = os.path.dirname(__file__)
face_list_file = os.path.join(current_path, 'face_list.txt')

#this is the function used to show the table containing present, absent and history data of the user
#which is ordered by date, and the roll number of the user
def index(request):
    scanned = LastFace.objects.all().order_by('date').reverse()
    present = Student_profile.objects.filter(present=True).order_by('updated').reverse()
    absent = Student_profile.objects.filter(present=False).order_by('roll_number')
    context = {
        'scanned': scanned,
        'present': present,
        'absent': absent,
    }
    return render(request, 'main/index.html', context)

#it renders the user to the start page of the project
def start(request):
    return render(request, 'main/start.html', {})

#it fetches the last face and renders the user to another last page web page
def lastface(request):
    last_face = LastFace.objects.last()
    context = {
        'last_face': last_face
    }
    return render(request, 'main/ajax.html', context)

#it is one of the main functions used for the final implementation 
#when user clicks on "Take Attendance" this function is hit
def scan(request):

    global last_face

    known_face_encodings = []
    known_face_names = []

    profiles = Student_profile.objects.all()


    #this loop scrolls on all the profiles updated on the web portal and fetches the profile details for
    #face recognition
    for profile in profiles:
        person = profile.image
        image_of_person = face_recognition.load_image_file(f'media/{person}')
        person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
        known_face_encodings.append(person_face_encoding)
        known_face_names.append(f'{person}'[:-4])


    video_capture = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

#an infinite loop is run while the scanner is in use for face recognition 
#of the user in the camera
    while True:

        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                    profile = Student_profile.objects.get(Q(image__icontains=name))
                    if profile.present == True:
                        pass
                    else:
                        profile.present = True
                        profile.save()

                    if last_face != name:
                        last_face = LastFace(last_face=name)
                        last_face.save()
                        last_face = name
                    else:
                        pass

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 0.5, (255, 255, 255), 1)

        cv2.imshow('Video', frame)
        #to manually stop the scanner "q" key is pressed 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return HttpResponse('scanner closed', last_face)

#this function extracts all the profiles updated and returns it to the user
def profiles(request):
    profiles = Student_profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'main/student_profile.html', context)

#this function presents the details of the user in last face recognised by the scanner
def details(request):
    try:
        last_face = LastFace.objects.last()
        profile = Student_profile.objects.get(Q(image__icontains=last_face))
    except:
        last_face = None
        profile = None

    context = {
        'profile': profile,
        'last_face': last_face
    }
    return render(request, 'main/details.html', context)

#it renders the user to the add student page where a submission form is shown to the user
#here user needs to upload his recent image for face recognition and marking the attendance
def add_student(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_profile')
    
    context={'form':form}
    return render(request,'main/add_student.html',context)

#it is used to edit the user profile
def edit_student(request,id):
    profile = Student_profile.objects.get(id=id)
    form = StudentForm(instance=profile)
    if request.method == 'POST':
        form = StudentForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('student_profile')
    context={'form':form}
    return render(request,'main/add_student.html',context)

#it is used to delete the profile of the user
def delete_student(request,id):
    profile = Student_profile.objects.get(id=id)
    profile.delete()
    return redirect('student_profile')

#it deletes the history of all the last faces recognised by the scanner
def clear_history(request):
    history = LastFace.objects.all()
    history.delete()
    return redirect('index')

#it resets the user profiles from present to absent category
def reset(request):
    profiles = Student_profile.objects.all()
    for profile in profiles:
        if profile.present == True:
            profile.present = False
            profile.save()
        else:
            pass
    return redirect('index')
