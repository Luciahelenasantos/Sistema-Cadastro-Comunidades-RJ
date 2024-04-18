// script.js
document.getElementById('cadastroForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const nomeAssoc = document.getElementById('nome_assoc').value;
    const endereco = document.getElementById('endereco').value;
    const telefone = document.getElementById('telefone').value;
    const nomeCoord = document.getElementById('nome_coord').value;
  
    const data = {
        nome_assoc: nomeAssoc,
        endereco: endereco,
        telefone: telefone,
        nome_coord: nomeCoord
    };
  
    fetch('http://localhost:5000/cadastrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        alert('Cadastro criado com sucesso!');  // Alerta de sucesso
        fetchCadastros(); // Recarregar a lista de cadastros após adicionar um novo
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Erro ao criar cadastro: ' + error.message);  // Alerta de erro
    });
  });
  
  document.getElementById('formularioForm').addEventListener('submit', function(event) {
      event.preventDefault();
  
      const codAssoc = document.getElementById('cod_assoc').value;
      const pergunta = document.getElementById('pergunta').value;
      const resposta = document.getElementById('resposta').value;
  
      const data = {
          cod_assoc: codAssoc,
          pergunta: pergunta,
          resposta: resposta
      };
  
      fetch('http://localhost:5000/formularios', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          console.log('Success:', data);
          alert('Formulário adicionado com sucesso!');
      })
      .catch((error) => {
          console.error('Error:', error);
          alert('Erro ao adicionar formulário: ' + error.message);
      });
  });
  
  let currentPage = 1;
  const perPage = 5;
  
  document.getElementById('searchForm').addEventListener('submit', function(event) {
      event.preventDefault();
      fetchCadastros();
  });
  
  function fetchCadastros() {
      const nomeAssoc = document.getElementById('searchInput').value;
      fetch(`http://localhost:5000/cadastros?nome_assoc=${nomeAssoc}&page=${currentPage}&per_page=${perPage}`)
          .then(response => response.json())
          .then(data => {
              displayCadastros(data.cadastros);
              updatePagination(data.current_page, data.pages);
          })
          .catch(error => console.error('Error:', error));
  }
  
  function displayCadastros(cadastros) {
      const container = document.getElementById('cadastrosContainer');
      container.innerHTML = ''; // Clear previous results
      cadastros.forEach(cadastro => {
          const div = document.createElement('div');
          div.innerHTML = `<strong>Nome:</strong> ${cadastro.nome_assoc}, <strong>Endereço:</strong> ${cadastro.endereco} <strong>Telefone:</strong> ${cadastro.telefone}<br>`;
          
          // Adicionando os formulários relacionados
          if (cadastro.formularios && cadastro.formularios.length > 0) {
              const ul = document.createElement('ul');
              cadastro.formularios.forEach(formulario => {
                  const li = document.createElement('li');
                  li.innerHTML = `<strong>Pergunta:</strong> ${formulario.pergunta} <strong>Resposta:</strong> ${formulario.resposta}`;
                  ul.appendChild(li);
              });
              div.appendChild(ul);
          } else {
              div.innerHTML += '<strong>Nenhum formulário relacionado encontrado.</strong>';
          }
  
          container.appendChild(div);
      });
  }
  
  function updatePagination(current, total) {
      const currentPageSpan = document.getElementById('currentPage');
      currentPageSpan.textContent = `Página ${current} de ${total}`;
      currentPage = current;
  }
  
  function changePage(step) {
      currentPage += step;
      fetchCadastros();
  }
  
  fetchCadastros();  // Initial fetch when page loads
  
  document.getElementById('deleteForm').addEventListener('submit', function(event) {
      event.preventDefault();
  
      const nomeAssoc = document.getElementById('deleteInput').value;
  
      fetch(`http://localhost:5000/cadastro/${nomeAssoc}`, {
          method: 'DELETE'
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('Falha ao deletar cadastro, resposta da rede não foi OK.');
          }
          return response.json();
      })
      .then(data => {
          console.log('Deleção realizada com sucesso:', data);
          alert('Cadastro deletado com sucesso!');
          fetchCadastros();  // Atualizar a lista de cadastros se necessário
      })
      .catch((error) => {
          console.error('Erro:', error);
          alert('Erro ao deletar cadastro.');
      });
  });
  
  // Atualiza os cadastros a cada 30 segundos
  document.getElementById('refreshButton').addEventListener('click', function() {
      fetchCadastros();
  });
  
  // Atualiza os cadastros automaticamente a cada 30 segundos
  setInterval(fetchCadastros, 30000);