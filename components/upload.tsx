"use client";

export default function Upload()
{
      const handleFileChange = async (event: any) => {
        const fileInput = event.target;
        if (!fileInput.files) {
          alert("no file was chosen");
          return;
        }

        if (!fileInput.files || fileInput.files.length === 0) {
          alert("files list is empty");
          return;
        }
        const selectedFile = event.target.files[0];
        const formData = new FormData();
        formData.set('file', selectedFile);
        try {
        const response = await fetch('/api/python', {
            method: 'POST',
            body: formData,
          });
          const data=await response.json();
          console.log(data);
          if (response.ok) {
            alert('File uploaded successfully!');
          } else {
            alert('Failed to upload file.');
          }
        }
        catch (error) {
            alert('Error uploading file:');
          }

      };

    return (
        <div className="w-full p-14 flex flex-col stretch items-center">
    
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="hidden"
            id="file-upload"
          />
          <label htmlFor="file-upload" className=" bg-blue-900 hover:bg-blue-950 fixed bottom-0 rounded mb-8 shadow-xl p-4 text-center text-white">
            Upload PDF
          </label>

      </div>
    );
}