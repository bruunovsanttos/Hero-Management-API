import "./Login.css";

function Login() {
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

        <form className="login-form">
          <div className="form-group">
            <label htmlFor="email">E-mail</label>

            <input
              type="email"
              id="email"
              placeholder="Digite seu e-mail"
            />
          </div>

          <div className="form-group">
            <label htmlFor="senha">Senha</label>

            <input
              type="password"
              id="senha"
              placeholder="Digite sua senha"
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