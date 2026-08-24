import { useState } from "react";
import { BarChart3, Eye, EyeOff, Lock, Mail } from "lucide-react";

export default function Login() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <main className="login-page">
      <section className="login-brand">
        <div className="brand-content">
          <div className="brand-logo">
            <BarChart3 size={30} />
          </div>

          <h1>Sales Analytics</h1>

          <p>
            Transforme dados de vendas em decisões estratégicas.
          </p>

          <div className="brand-stats">
            <div>
              <strong>100k+</strong>
              <span>pedidos analisados</span>
            </div>

            <div>
              <strong>15k</strong>
              <span>clientes</span>
            </div>
          </div>
        </div>
      </section>

      <section className="login-area">
        <div className="login-card">
          <div className="login-header">
            <span className="login-label">PLATAFORMA ANALYTICS</span>

            <h2>Bem-vindo de volta</h2>

            <p>
              Entre na sua conta para acessar o dashboard.
            </p>
          </div>

          <form>
            <label>
              E-mail

              <div className="input-wrapper">
                <Mail size={19} />

                <input
                  type="email"
                  placeholder="seu@email.com"
                />
              </div>
            </label>

            <label>
              Senha

              <div className="input-wrapper">
                <Lock size={19} />

                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Digite sua senha"
                />

                <button
                  type="button"
                  className="password-button"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeOff size={19} />
                  ) : (
                    <Eye size={19} />
                  )}
                </button>
              </div>
            </label>

            <div className="login-options">
              <label className="remember">
                <input type="checkbox" />
                Lembrar de mim
              </label>

              <button type="button" className="forgot-password">
                Esqueci minha senha
              </button>
            </div>

            <button type="submit" className="login-button">
              Entrar na plataforma
            </button>
          </form>

          <p className="login-footer">
            Sales Analytics Platform • Full Stack Data Solution
          </p>
        </div>
      </section>
    </main>
  );
}