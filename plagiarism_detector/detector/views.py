from django.shortcuts import render, redirect
from .models import FileRepository
import os
from django.http import HttpResponse
from docx import Document  # Optimized import for readability
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .forms import FileRepositoryIForm
from .models import FileRepositoryI
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from django.contrib.auth.models import User
from django.core.mail import send_mail





def home(request):
       return render(request, 'index.html')

     
def about(request):
       return render(request, 'about.html')


# for feedback page
def feedback_view(request):
    return render(request, 'feedback.html')


def coordinator(request):
    #update_status()
    count=0
    notifications=Notification.objects.all()
    if notifications:
       for notification in notifications:
          if notification.read==False:
            count =count+1
       return render(request, 'coordinator.html', {'notfication': count})              
    return render(request, 'coordinator.html')


def file_repo(request):
    #update_status()
    files = FileRepositoryI.objects.all()
    return render(request, 'fle_repo.html', {'files': files})



def download_file(request, file_id):
    file_repository = get_object_or_404(FileRepositoryI, id=file_id)
    file_path = file_repository.file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + file_repository.file.name
        return response


def user(request):
     
     if request.method == 'GET':
        search_query = request.GET.get('search_term')

        if search_query:
            # Perform case-insensitive search using icontains
            search_results = FileRepositoryI.objects.filter(
                Q(catagory__icontains=search_query) | Q(file_name__icontains=search_query)|Q(author__icontains=search_query) |Q(college__icontains=search_query) # Search both title and filename
             ,status='accepted')
            print(search_results)
        else:
            search_results = []  # Empty list if no search query
       
        print(search_results)
        return render(request, 'student_and_reeasercher.html', {'search_results': search_results})
     
     return render(request, 'student_and_reeasercher.html')


def contact(request):
       return render(request, 'contact.html')




# def feedback_view(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             feedback = form.save(commit=False)
#             feedback.user = request.user
#             feedback.save()
#             messages.success(request, 'Thank you for your feedback!')
           
#             success_message ="thank you for your feedback"
#             form = FeedbackForm()
#             return render(request, 'feedback.html', {'form': form, 'success_message': success_message})
#             # return redirect('contact')
#     else:
#         form = FeedbackForm()

#     # success_message ="thank you for your feedback"
#     # messages.get_messages(request)
#     return render(request, 'feedback.html',{'form': form,})





def upload_file(request):
    
    if request.method == 'POST':
        college = request.POST.get('college')
        department = request.POST.get('department')
        author = request.POST.get('author')
        degree_level = request.POST.get('Degree')
        catagory = request.POST.get('Catagory')
        file_name = request.FILES['file_name']
        
        # Create and save the model instance
        file_repository = FileRepositoryI(
            user=request.user,  # Assuming you have authentication enabled
            college=college,
            department=department,
            author=author,
            degree_level=degree_level,
            catagory=catagory,
            file_name=file_name
        )
        file_repository.save()
        email_message='New file uloaded by User'
        staff_members = User.objects.filter(is_staff=True)
        for user in staff_members:
         send_custom_email(user.email,email_message)
           
        return render(request, 'file_upload.html', {'success_message': 'File Uploaded succesfully!'})
        
        #return redirect('success')  # Redirect to a success page after saving the instance
    
    return render(request, 'file_upload.html')  # Render the upload form initially



def upload_file_for_plagiarism_check(request):
    if request.method == 'POST':
        file = request.FILES['file']

        # Preprocess the uploaded file
        uploaded_text = preprocess_file(file)

        # Perform plagiarism check with the database
        plagiarism_results = check_plagiarism_with_database(uploaded_text)

        return render(request, 'plagiarism_result.html', {'plagiarism_results': plagiarism_results})
    return render(request, 'home.html')

def plagiarism_check(request, file_id):
        file = get_object_or_404(FileRepositoryI, id=file_id)
        #file_path = file_repository.file_name
        # Save the changes to the database
        message=""
        print(file.user.email)
        if file:
        # Preprocess the uploaded file
           
           uploaded_text = preprocess_file(file.file_name)
            
        # Perform plagiarism check with the database
           plagiarism_result = check_plagiarism_with_database(uploaded_text)
           print(plagiarism_result)
           if plagiarism_result[1] >= 0.75:
                   file.status = 'rejected'  # Update the status to 'accepted'
                   file.save() 
                   message='File uploaded to HURP has been rejected'
                   send_custom_email(file.user.email,message)
                   result=plagiarism_result[0]
                   print(result)
                   return render(request, 'plagiarism_result.html', {'plagiarism_results': result})
           else:
                    message='File uploaded to HURP has been rejected'
                    file.status = 'accepted'  # Update the status to 'accepted'
                    file.save() 
                    send_custom_email(file.user.email,message)
        return render(request, 'plagiarism_result.html', {'plagiarism_results': plagiarism_result[0]})




def plagiarism_result(request):
    # Access plagiarism results from the view function (if needed)
    plagiarism_results = request.context.get('plagiarism_results')
    return render(request, 'plagiarism_result.html', {'plagiarism_results': plagiarism_results})




def check_plagiarism_with_database(uploaded_text):
  plagiarism_results = []
  similarity_score = 0
    # Iterate through all files in the database
  for database_file in FileRepositoryI.objects.all():
    if database_file.status=="accepted":
        reference_text = preprocess_file(database_file.file_name)

        # Calculate cosine similarity for plagiarism detection
        similarity_score = calculate_similarity(uploaded_text, reference_text)

        # Set a threshold for plagiarism (adjust as needed)
        plagiarism_threshold = 0.75  # Example threshold, adjust based on your needs

        if similarity_score >= plagiarism_threshold: 
        # Convert cosine similarity to percentage (multiply by 100)
          similarity_percent = similarity_score * 100

      # Format similarity score with four decimal places
          formatted_score = "{:.4f}".format(similarity_score)

          plagiarism_results.append({
            'catagory': database_file.catagory,
            'filename': database_file.file_name,
            'similarity_score': formatted_score,  # Use formatted score
            'similarity_percent': f"{similarity_percent:.2f}%"  # Format as percentage with 2 decimals
          })
          print(plagiarism_result)
  
  return plagiarism_results, similarity_score



def preprocess_file(file):
    """
    Extracts text from various file types (doc, docx, pdf, txt) for plagiarism checking.

    Args:
        file: The uploaded file object.

    Returns:
        str: The preprocessed text content of the file.
    """

    text = ''
    filename, file_extension = os.path.splitext(file.name)

    if file_extension in ['.doc', '.docx']:
        # Read doc/docx files
        document = Document(file)
        for paragraph in document.paragraphs:
            text += paragraph.text.strip()  # Remove leading/trailing whitespace
    elif file_extension == '.pdf':
        # Read PDF files
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text().strip()  # Remove leading/trailing whitespace
    elif file_extension == '.txt':
        # Read text files
        text = file.read().decode('utf-8').strip()  # Read as UTF-8 and remove whitespace
    else:
        # Handle unsupported file types (raise an exception or log a warning)
        raise ValueError(f"Unsupported file type: {file_extension}")

    # Additional preprocessing steps can be added here (e.g., lowercase conversion, stop word removal)
   
    return text



def calculate_similarity(text1, text2):
    """
    Calculates cosine similarity between two text strings using CountVectorizer and cosine_similarity.

    Args:
        text1: The first text string.
        text2: The second text string.

    Returns:
        float: The cosine similarity score between the two texts.
    """

    vectorizer = CountVectorizer()
    vectorized_text = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(vectorized_text)[0][1]
    return similarity


def update_status():
    file_repository = FileRepositoryI.objects.get(id=18)
    file_repository.status = 'accepted'  # Update the status to 'accepted'
    file_repository.save()  # Save the changes to the database




@receiver(post_save, sender=FileRepositoryI)
def notify_coordinators(sender, instance, created, **kwargs):
    if created:
        coordinators = User.objects.filter(is_staff=True)
        for coordinator in coordinators:
            Notification.objects.create(
                recipient=coordinator,
                message=f"A new file has been uploaded by {instance.user.username}."
            )


def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()
    notifications=Notification.objects.filter(read=False)
    return render(request, 'notfication.html', {'notifications': notifications})

def notification_view_read(request):
    notifications=Notification.objects.filter(read=False)
    return render(request, 'notfication.html', {'notifications': notifications})



def open_file(request, file_id):
    file_repository = get_object_or_404(FileRepositoryI, id=file_id)
    file_path_byte = file_repository.file_name
    file_path = file_path_byte.read()
    return render(request, 'open_file.html', {'file_path': file_path})



def send_custom_email(email_acc, message):
    subject = "Deear "
    message = message
    recipient_list = [email_acc]
    send_mail(subject, message, "suraatte@gmail.com", recipient_list)  