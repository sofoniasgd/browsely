document.addEventListener('DOMContentLoaded', () => {
    
});

document.getElementById('search_button').addEventListener('click', () => {
    const alertBox = document.getElementById('alert-box');
    // Get the search query
    const tinNumber = document.getElementById('input').value.trim();
    // check if the search query is correct
    if (!/^\d{10}$/.test(tinNumber)) {
        // wrong TIN format alert
        createAutoCloseAlert('warning', 'please enter a valid <strong>TIN</strong> number/እባክዎ ትክክለኛ ቲን ያስገቡ!');
    } else {
        // clear the alert box
        alertBox.innerHTML = '';
        // display the loading spinner in the result container
        const resultContainer = document.getElementById('result-container');
        resultContainer.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-info" style="width: 5rem; height: 5rem;" role="status">
                </div>
            </div>
            <div class="text-center">
                <span class="text-info">Loading/በፍለጋ ላይ</span>
            </div>
            `;
        // fetch results
        fetch(`/search/${tinNumber}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if(data.error) {
                    // display the 'no record' message and show alert 
                    createAutoCloseAlert('danger', "TIN not found/ባስገቡት ቲን መረጃ አልተገኘም");
                    resultContainer.innerHTML = '';
                    resultContainer.innerHTML = `
                        <div class="text-center">
                            <img src="static/images/no_record.png" alt="No record found">
                            <p class="text-center">Record not found/መረጃ አልተገኘም</p>
                        </div>
                    `;
                } else {
                    //clear the result container
                    resultContainer.innerHTML = '';
                    // display the result in a table where file names are buttons to launch viewer page
                    resultContainer.innerHTML = `
                        <table class="table table-striped table-hover table-info">
                            <thead>
                                <tr>
                                    <th scope="col">File Names/የፋይል ዝርዝር</th>
                                    <th scope="col">Location/የፋይሉ መገኛ</th>
                                </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        </table>
                    `;
                    const tableBody = resultContainer.querySelector('tbody');
                    data.forEach(file => {
                        const row = document.createElement('tr');
                        // insert results as buttons to launch viewer page
                        row.innerHTML = `
                            <td><button class="btn btn-outline-secondary" onclick="displayPdf('${file.name}', 'result-container')">${file.name}</button></td>
                            <td>${file.location}</td>
                        `;
                        tableBody.appendChild(row);
                    });
                }
            })
    }
});


// creates alerts
function createAutoCloseAlert(type, message, timeout = 5000) {
    const alertContainer = document.getElementById('alert-box');
    existingAlert = document.getElementById('alertid');
    // remove existing alert if user is button happy
    if (existingAlert) {
      existingAlert.remove();
    }
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.id = 'alertid';
    alertDiv.innerHTML = `
      <img src = "static/images/exclamation-circle.svg"/>
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    console.log('added alert to the alert box');
    alertContainer.appendChild(alertDiv);
    // Automatically close the alert after timeout
    setTimeout(() => {
      console.log('closing alert in ${timeout}ms');
      alertDiv.remove();
    }, timeout);
  }
  

// pdf display function
function displayPdf(pdfName, container) {
    console.log('pdfPath:', pdfName);
    // open the pdf_viewer window to display the pdf
    const pdfUrl = `/download/${pdfName}`;
    window.open(pdfUrl, "_blank");
  }