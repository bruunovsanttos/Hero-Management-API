import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(
        "https://hero-management-api.onrender.com/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
            senha,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        console.error("Erro no login:", data);
        return;
      }

      localStorage.setItem("access_token", data.access_token);

      console.log("Login realizado com sucesso!");

      const usuarioResponse = await fetch(
        "https://hero-management-api.onrender.com/auth/me",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${data.access_token}`,
          },
        }
      );

      const usuario = await usuarioResponse.json();

      console.log("Usuário autenticado:", usuario);

      navigate("/dashboard");


    } catch (error) {
      console.error("Erro ao realizar login:", error);
    }
  };

  return (
    <main className="login-page">
      <section className="login-card">
        <div className="login-header">
          <span className="login-badge">HERO MANAGEMENT</span>

          <h1>Central de Operações</h1>

          <p>
            Acesse o sistema para gerenciar heróis, ameaças e missões.
          </p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">E-mail</label>

            <input
              type="email"
              id="email"
              placeholder="Digite seu e-mail"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="senha">Senha</label>

            <input
              type="password"
              id="senha"
              placeholder="Digite sua senha"
              value={senha}
              onChange={(event) => setSenha(event.target.value)}
            />
          </div>

          <button type="submit">
            Entrar
          </button>
        </form>
      </section>
    </main>
  );
}

export default Login;