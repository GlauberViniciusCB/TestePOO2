const container = document.getElementById("container");
const registroBtn = document.getElementById("registrar");
const loginBtn = document.getElementById("login");

registroBtn.addEventListener('click',() =>{
    container.classList.add("ativo");
} );

loginBtn.addEventListener("click", () =>{
    container.classList.remove("ativo");
});

function mudarPagina(pagina){
    
    const menuItems = document.querySelectorAll('.menuItem');
    menuItems.forEach(item => item.classList.remove('ativoMenu'));
    
    document.getElementById(pagina).classList.add('ativoMenu');
    
    const conteudo = document.querySelector('.conteudo');
    conteudo.innerHTML = '';

    if (pagina === 'clientes') {
        showClientesFormulario();
    }
    else if (pagina === 'pacientes') {
        showPacientesFormulario();
    } 
    else if (pagina === 'consultas') {
        showConsultasFormulario();
    }
}


// Registrar

document.getElementById("formRegistrar").addEventListener("submit", function(event) {
    event.preventDefault();

    // Coletando os valores dos campos no momento do submit
    const nomeRegistrar = document.getElementById("RegistrarNome").value;
    const emailRegistrar = document.getElementById("RegistrarEmail").value;
    const senhaRegistrar = document.getElementById("RegistrarSenha").value;
    const confirmarSenhaRegistrar = document.getElementById("RegistrarConfirmeSenha").value;

    // Verificação de senhas
    if (senhaRegistrar !== confirmarSenhaRegistrar) {
        alert("As senhas não coincidem!");
        return;
    }

    // Preparando os dados para envio
    const dados = {
        nome: nomeRegistrar,
        email: emailRegistrar,
        senha: senhaRegistrar
    };

    // Enviando a requisição
    fetch("http://127.0.0.1:8000/registrarVeterinario", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById("RegistrarNome").value = '';
        document.getElementById("RegistrarEmail").value = '';
        document.getElementById("RegistrarSenha").value = '';
        document.getElementById("RegistrarConfirmeSenha").value = '';
    })
    .catch(error => {
        console.error("Erro ao registrar:", error);
        alert("Erro ao registrar no servidor!");
    });
});

async function obterNomeVeterinario() {
    try {
        const token = localStorage.getItem("access_token");  // Recupera o token do localStorage

        const response = await fetch('http://localhost:8000/getVeterinario', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`  // Envia o token no cabeçalho
            }
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('nomeVeterinario').innerHTML = `Bem-Vindo, ${data.nome}!`;
        } else {
            alert('Veterinário não autenticado!');
        }
    } catch (error) {
        console.error('Erro ao buscar o nome do veterinário:', error);
        alert('Erro no servidor. Tente novamente mais tarde.');
    }
}


// Entrar // função correta 

document.getElementById("formLogin").addEventListener("submit", function(event) {
    event.preventDefault();

    // Pegando os valores dos campos de login
    const emailLogin = document.getElementById("entrarEmail").value;
    const senhaLogin = document.getElementById("entrarSenha").value;

    // Preparando os dados para enviar como JSON
    const dados = {
        email: emailLogin,
        senha: senhaLogin
    };

    // Enviando a requisição com o corpo em JSON
    fetch("http://127.0.0.1:8000/loginVeterinario", {
        method: "POST",
        headers: {
            "Content-Type": "application/json", 
        },
        body: JSON.stringify(dados) 
    })
    .then(response => response.json()) 
    .then(data => {
        alert(data.message); 
        if (data.message === "Login bem-sucedido!") {  
            // Armazenando o token no localStorage
            localStorage.setItem("access_token", data.access_token);
            obterNomeVeterinario()
           
            window.location.href = "/home"; 
        }
    })
    .catch(error => {
        console.error("Erro ao logar:", error); 
        alert("Erro ao fazer login!"); 
    });
});



// Função para mostrar a lista de clientes
async function mostrarClientes() {
    try {
        const response = await fetch('http://127.0.0.1:8000/clientes');
        const result = await response.json();
        const clientes = result.clientes; 

        const clientList = document.getElementById('clientList');
        clientList.innerHTML = ''; 

        clientes.forEach(cliente => {
            const li = document.createElement('li');
            li.className = 'list-item';
            li.innerHTML = `Nome: ${cliente[1]} | Telefone: ${cliente[3]} | Endereço: ${cliente[2]} |  Email: ${cliente[4]}`;
            clientList.appendChild(li);
        });
    } catch (error) {
        console.error('Erro ao carregar os clientes:', error);
    }
}

// Função para cadastrar um cliente
async function addCliente() {
    const nome = document.getElementById('clienteNome').value;
    const email = document.getElementById('clienteEmail').value;
    const endereco = document.getElementById('clienteEnd').value;
    const telefone = document.getElementById('clienteTel').value;

    if (nome && email && endereco && telefone) {
        const cliente = {
            nome: nome,
            email: email,
            endereco: endereco,
            telefone: telefone
        };

        try {
          
            const response = await fetch('http://127.0.0.1:8000/registrarCliente', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(cliente)
            });

            const result = await response.json();
            console.log(result); 

            if (response.ok) {
                alert(result.message);
                
                
                document.getElementById('clienteNome').value = '';
                document.getElementById('clienteEmail').value = '';
                document.getElementById('clienteEnd').value = '';
                document.getElementById('clienteTel').value = '';

                
                mostrarClientes();
            } else {
                alert('Erro ao cadastrar cliente.');
            }

        } catch (error) {
            alert('Erro ao se comunicar com o servidor.');
        }
    } else {
        alert('Por favor, preencha todos os campos.');
    }
}

// Carregar a lista de clientes ao carregar a página
window.onload = function() {
    mostrarClientes();
};

// Função para exibir o formulário
function showClientesFormulario() {
    const conteudo = document.getElementById('conteudo');
    conteudo.innerHTML = `
        <h1>Cadastro de Cliente</h1>
        <div class="form-container">
            <input type="text" id="clienteNome" placeholder="Nome do Cliente" required>
            <input type="email" id="clienteEmail" placeholder="Email do Cliente" required>
            <input type="text" id="clienteEnd" placeholder="Endereço do Cliente" required>
            <input type="tel" id="clienteTel" placeholder="Telefone do Cliente" required> 
            <button onclick="addCliente()">Cadastrar Cliente</button>
        </div>
        <div class="list-container">
            <div class="list-title">Clientes Cadastrados</div>
            <ul class="list" id="clientList"></ul>
        </div>
    `;
}


async function mostrarPaciente() {
    try{
        const response = await fetch('http://127.0.0.1:8000/pacientes');
        const result = await response.json();
        const pacientes = result.pacientes;

        const pacienteList = document.getElementById('patientList');
        pacienteList.innerHTML = '';

       
        const tutoresResponse = await fetch('/tutores');
        const tutoresData = await tutoresResponse.json();
        const tutoresMap = new Map(tutoresData.tutores.map(tutor => [tutor.id_cliente, tutor.nome]));

        pacientes.forEach(paciente => {
            const tutorNome = tutoresMap.get(paciente[1]);  

            const li = document.createElement('li');
            li.className = 'list-item';
            li.innerHTML = `Tutor: ${tutorNome} | Nome: ${paciente[2]} | Espécie: ${paciente[3]} | Raça: ${paciente[4]} | Idade: ${paciente[5]} Meses | Sexo: ${paciente[6]}`;
            pacienteList.appendChild(li);
        });
    } catch (error) {
        console.error('Erro ao carregar os pacientes', error);
    }
}


function showPacientesFormulario() {
    const conteudo = document.getElementById('conteudo');
    conteudo.innerHTML = `
        <h1>Cadastro de Paciente</h1>
        <div class="form-container">
            <select name="tutorPaciente" id="tutorPaciente" required>
                <option value="" disabled selected>Selecione o tutor do paciente</option>
            </select>
            <input type="text" id="pacienteNome" placeholder="Nome do Paciente" required>
            <input type="text" id="pacienteEspecie" placeholder="Espécie do Paciente" required>      
            <input type="text" id="pacienteRaca" placeholder="Raça do Paciente" required>
            <input type="number" id="pacienteIdade" placeholder="Idade do Paciente em Meses" required min="0" step="1">
            <select name="PacienteSexo" id="pacienteSexo" required>
                <option value="" disabled selected>Selecione o sexo do paciente</option>
                <option value='M'>Macho</option>
                <option value="F">Fêmea</option>
            </select>
            <button onclick="addPaciente()">Cadastrar Paciente</button>
        </div>
        <div class="list-container">
            <div class="list-title">Pacientes Cadastrados</div>
            <ul class="list" id="patientList"></ul>
        </div>
    `;

    
    mostrarPaciente();

    
    fetch('/tutores')
        .then(response => response.json())
        .then(data => {
            const selectTutor = document.getElementById('tutorPaciente');
            data.tutores.forEach(tutor => {
                const option = document.createElement('option');
                option.value = tutor.id_cliente;
                option.textContent = tutor.nome;
                selectTutor.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Erro ao buscar tutores:', error);
        });
}


async function addPaciente() {
    const tutorId = document.getElementById('tutorPaciente').value;  
    const pacienteNome = document.getElementById('pacienteNome').value;
    const pacienteEspecie = document.getElementById('pacienteEspecie').value;
    const pacienteRaca = document.getElementById('pacienteRaca').value;
    const pacienteIdade = document.getElementById('pacienteIdade').value;
    const pacienteSexo = document.getElementById('pacienteSexo').value;

  
    if (!tutorId) {
        alert("Por favor, selecione um tutor.");
        return; 
    }

    const paciente = {
        tutor: tutorId,  
        nome: pacienteNome,
        especie: pacienteEspecie,
        raca: pacienteRaca,
        idade: pacienteIdade,
        sexo: pacienteSexo
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/registrarPaciente', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(paciente)
        });

        const result = await response.json();
        if (result.message) {
            alert('Paciente cadastrado com sucesso!');
        } else {
            alert('Erro ao cadastrar paciente.');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao tentar cadastrar paciente.');
    }
}




function showConsultasFormulario() {
    const conteudo = document.getElementById('conteudo');
    conteudo.innerHTML = `
        <h1>Cadastro de Consulta</h1>
        <div class="form-container">
            <select name="consultaVet" id="consultaVet" required>
                <option value="" disabled selected>Selecione o veterinário</option>
            </select>
            <select name="consultaPaciente" id="consultaPaciente" required>
                <option value="" disabled selected>Selecione o paciente</option>
            </select>
            <input type="date" id="consultaData" required>
            <input type="time" id="consultaHora" required>
            <button onclick="addConsulta()">Cadastrar Consulta</button>
        </div>
        <div class="list-container">
            <div class="list-title">Consultas Agendadas</div>
            <ul class="list" id="consultationList"></ul>
        </div>
    `;

    mostrarConsultas();

    fetch('/listarVeterinarios')
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const selectVeterinario = document.getElementById('consultaVet');
            data.veterinarios.forEach(veterinario => {
                const option = document.createElement('option');
                option.value = veterinario.id_veterinario;
                option.textContent = veterinario.nome;
                selectVeterinario.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Erro ao buscar veterinário', error);
        });
        
    // Buscar lista de pacientes
    fetch('/listarPacientes')
        .then(response => response.json())
        .then(data => {
            const selectPaciente = document.getElementById('consultaPaciente');
            data.pacientes.forEach(paciente => {
                const option = document.createElement('option');
                option.value = paciente.id_animal;
                option.textContent = paciente.nome;
                selectPaciente.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Erro ao buscar pacientes', error);
        });
}



async function mostrarConsultas() {
    try {
        const response = await fetch('http://127.0.0.1:8000/consultas');
        const result = await response.json();
        const consultas = result.consultas;

        const consultationList = document.getElementById('consultationList');
        consultationList.innerHTML = ''; 

        consultas.forEach(consulta => {
            const li = document.createElement('li');
            li.className = 'list-item';
            
            li.innerHTML = `Veterinário: ${consulta.nome_veterinario} | Paciente: ${consulta.nome_animal} | Data: ${consulta.data_consulta} | Hora: ${consulta.hora_consulta}`;
            consultationList.appendChild(li);
        });
    } catch (error) {
        console.error('Erro ao carregar as consultas', error);
    }
}


async function addConsulta() {
    const vetNome = document.getElementById('consultaVet').value;
    const pacienteId = document.getElementById('consultaPaciente').value;
    const consultaData = document.getElementById('consultaData').value;
    const consultaHora = document.getElementById('consultaHora').value;

    if (!vetNome || !pacienteId || !consultaData || !consultaHora) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    const consulta = {
        animal: pacienteId,
        veterinario: vetNome,
        data: consultaData,
        hora: consultaHora,
        status: 'agendada'
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/registrarConsulta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(consulta)
        });

        const result = await response.json();

        if (response.ok) {
            alert('Consulta cadastrada com sucesso!');
            mostrarConsultas();  // Atualiza a lista de consultas
        } else {
            alert('Erro ao cadastrar consulta: ' + result.detail || result.message);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao tentar cadastrar consulta.');
    }
}




