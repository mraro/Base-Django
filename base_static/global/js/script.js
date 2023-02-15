function my_scope(){
    const forms = document.querySelectorAll('.form-to-delete');
    for( const form of forms){
        form.addEventListener('submit', function(e) {
            e.preventDefault();  // evita o que aconteceria normalmente

            const confirmed = confirm("Tem certeza?")

            if (confirmed) {
                form.submit();
            }
        });
    } 
}
my_scope();