const url = 'http://127.0.0.1:5000/empregados'


fetch(url)
  .then(response => {    
    return response.json();
  })
  .then(empregados => {
    
    console.log('Empregados:', empregados);
  })
  .catch(error => {
    console.error('Error:', error);
  });