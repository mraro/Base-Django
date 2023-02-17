function delete_alert() {
    const forms = document.querySelectorAll('.form-delete');
  
    for (const form of forms) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
  
        const confirmed = confirm('Tem certeza que deseja apagar?');
  
        if (confirmed) {
          form.submit();
        }
      });
    }
  }
  
  delete_alert();