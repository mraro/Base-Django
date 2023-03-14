// THIS ASK IF WANTS TO DELETE FOR SURE ON DASHBOARD USER
(() => {
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
  
})();

(() => {
  // THIS CHECK IF HAS IMAGE ON FIELD, ELSE ASK IF WANTS CONTINUE ON FORM FROM DASHBOARD

  function hasClass(element) {
    return (element) == null;
  }

  const imageInput = document.querySelector('.image-object');
  const imageView = document.querySelector('.remedio-img');
  const form = document.querySelector('.form-content');
  // event listener avoid save before test if has image
  form.addEventListener('submit', function (e) {
    if (imageInput.files.length != 1){
        console.log("Create")
        // this case in create mode because don't have imageView.src and avoid error
          if (hasClass(imageView)){          
              e.preventDefault();
              
              const confirmed = confirm("Image filed is empty, you sure?") ;
              if (confirmed){   form.submit();    }
              
          }else if(imageView.src == "http://127.0.0.1:8000/media/static/images/default.jpg"){
            console.log("Edit")
            e.preventDefault();
            
            const confirmed = confirm("Image filed is empty, you sure?") ;
              if (confirmed){   form.submit();    }
            
          }
      }
    
  });
})();
