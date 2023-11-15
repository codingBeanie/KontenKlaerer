from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage


def pageData(request):
    if request.method == "POST":
        file = request.FILES["file_upload"]
        file_name = default_storage.save(file.name, file)
        message = "Datei hochgeladen: " + file_name

    else:
        message = "Wählen Sie eine CSV-Datei für den Upload aus."

    return render(request, "pageData.html", {"message": message})
