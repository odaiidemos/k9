import { useState, FormEvent } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { useLogin } from '@services/auth/authService';
import { useAppSelector } from '@store/hooks';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mfaToken, setMfaToken] = useState('');
  const [showMfa, setShowMfa] = useState(false);
  const { isAuthenticated } = useAppSelector((state) => state.auth);
  
  const loginMutation = useLogin();

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    try {
      const result = await loginMutation.mutateAsync({
        username,
        password,
        mfa_token: showMfa ? mfaToken : undefined,
      });

      if (result.mfa_required) {
        setShowMfa(true);
      }
    } catch (error) {
      console.error('Login failed:', error);
      // If MFA fails, reset the form to allow retry
      if (showMfa) {
        setMfaToken('');
      }
    }
  };

  const handleCancelMfa = () => {
    setShowMfa(false);
    setMfaToken('');
    setUsername('');
    setPassword('');
  };

  return (
    <div className="container-fluid vh-100">
      <div className="row h-100">
        <div className="col-lg-6 d-none d-lg-flex align-items-center justify-content-center bg-primary">
          <div className="text-center text-white px-5">
            <i className="fas fa-shield-dog fa-5x mb-4"></i>
            <h1 className="display-4 mb-3">نظام إدارة عمليات الكلاب البوليسية</h1>
            <p className="lead">
              نظام شامل ومتقدم لإدارة جميع جوانب عمليات الكلاب البوليسية والعسكرية
              من التدريب والرعاية إلى التكاثر والمهام الميدانية
            </p>
          </div>
        </div>

        <div className="col-lg-6 d-flex align-items-center justify-content-center">
          <div className="card shadow-lg border-0" style={{ maxWidth: '500px', width: '100%' }}>
            <div className="card-body p-5">
              <div className="text-center mb-4">
                <i className={`fas ${showMfa ? 'fa-key' : 'fa-shield-alt'} fa-3x text-primary mb-3`}></i>
                <h2 className="card-title">{showMfa ? 'المصادقة الثنائية' : 'تسجيل الدخول'}</h2>
                <p className="text-muted">
                  {showMfa 
                    ? 'أدخل رمز المصادقة الثنائية من تطبيق Authenticator'
                    : 'أدخل بيانات الاعتماد الخاصة بك للوصول إلى النظام'}
                </p>
              </div>

              {showMfa && (
                <div className="alert alert-info" role="alert">
                  <i className="fas fa-info-circle ms-2"></i>
                  تم تمكين المصادقة الثنائية لحسابك. افتح تطبيق Authenticator وأدخل الرمز المكون من 6 أرقام.
                </div>
              )}

              {loginMutation.isError && (
                <div className="alert alert-danger" role="alert">
                  <i className="fas fa-exclamation-circle ms-2"></i>
                  {showMfa 
                    ? 'رمز MFA غير صحيح. يرجى المحاولة مرة أخرى.'
                    : 'فشل تسجيل الدخول. يرجى التحقق من بيانات الاعتماد.'}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                {!showMfa ? (
                  <>
                    <div className="mb-3">
                      <label htmlFor="username" className="form-label">
                        <i className="fas fa-user ms-2"></i>
                        اسم المستخدم
                      </label>
                      <input
                        type="text"
                        className="form-control form-control-lg"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="أدخل اسم المستخدم"
                        required
                        disabled={loginMutation.isPending}
                        autoFocus
                      />
                    </div>

                    <div className="mb-3">
                      <label htmlFor="password" className="form-label">
                        <i className="fas fa-lock ms-2"></i>
                        كلمة المرور
                      </label>
                      <input
                        type="password"
                        className="form-control form-control-lg"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="أدخل كلمة المرور"
                        required
                        disabled={loginMutation.isPending}
                      />
                    </div>
                  </>
                ) : (
                  <div className="mb-3">
                    <label htmlFor="mfaToken" className="form-label">
                      <i className="fas fa-key ms-2"></i>
                      رمز المصادقة الثنائية (MFA)
                    </label>
                    <input
                      type="text"
                      className="form-control form-control-lg text-center"
                      id="mfaToken"
                      value={mfaToken}
                      onChange={(e) => setMfaToken(e.target.value.replace(/\D/g, ''))}
                      placeholder="أدخل رمز MFA المكون من 6 أرقام"
                      maxLength={6}
                      pattern="\d{6}"
                      required
                      disabled={loginMutation.isPending}
                      autoFocus
                      style={{ fontSize: '1.5rem', letterSpacing: '0.5rem' }}
                    />
                    <small className="text-muted d-block mt-2 text-center">
                      الرمز صالح لمدة 30 ثانية فقط
                    </small>
                  </div>
                )}

                <div className="d-grid mb-3">
                  <button
                    type="submit"
                    className="btn btn-primary btn-lg"
                    disabled={loginMutation.isPending || (showMfa && mfaToken.length !== 6)}
                  >
                    {loginMutation.isPending ? (
                      <>
                        <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>
                        {showMfa ? 'جارِ التحقق...' : 'جارِ تسجيل الدخول...'}
                      </>
                    ) : (
                      <>
                        <i className={`fas ${showMfa ? 'fa-check' : 'fa-sign-in-alt'} ms-2`}></i>
                        {showMfa ? 'تحقق' : 'دخول'}
                      </>
                    )}
                  </button>
                </div>

                {showMfa ? (
                  <div className="text-center">
                    <button
                      type="button"
                      className="btn btn-link text-decoration-none"
                      onClick={handleCancelMfa}
                      disabled={loginMutation.isPending}
                    >
                      <i className="fas fa-arrow-right ms-2"></i>
                      إلغاء والعودة لتسجيل الدخول
                    </button>
                  </div>
                ) : (
                  <div className="text-center">
                    <Link to="/password-reset" className="text-decoration-none">
                      <i className="fas fa-question-circle ms-2"></i>
                      نسيت كلمة المرور؟
                    </Link>
                  </div>
                )}
              </form>
            </div>

            <div className="card-footer bg-light text-center">
              <small className="text-muted">
                © 2025 نظام إدارة عمليات الكلاب البوليسية
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
