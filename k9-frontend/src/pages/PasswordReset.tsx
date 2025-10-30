import { useState, type FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { useRequestPasswordReset } from '@services/auth/passwordResetService';

const PasswordReset = () => {
  const [email, setEmail] = useState('');
  const resetMutation = useRequestPasswordReset();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await resetMutation.mutateAsync({ email });
    } catch (error) {
      // Errors are shown via mutation state
      console.error('Password reset request failed:', error);
    }
  };

  return (
    <div className="container-fluid vh-100">
      <div className="row h-100">
        <div className="col-lg-6 d-none d-lg-flex align-items-center justify-content-center bg-primary">
          <div className="text-center text-white px-5">
            <i className="fas fa-lock-open fa-5x mb-4"></i>
            <h1 className="display-4 mb-3">استعادة كلمة المرور</h1>
            <p className="lead">
              أدخل عنوان بريدك الإلكتروني وسنرسل لك تعليمات استعادة كلمة المرور
            </p>
          </div>
        </div>

        <div className="col-lg-6 d-flex align-items-center justify-content-center">
          <div className="card shadow-lg border-0" style={{ maxWidth: '500px', width: '100%' }}>
            <div className="card-body p-5">
              <div className="text-center mb-4">
                <i className="fas fa-key fa-3x text-primary mb-3"></i>
                <h2 className="card-title">نسيت كلمة المرور؟</h2>
                <p className="text-muted">
                  لا تقلق، سنساعدك في استعادة الوصول إلى حسابك
                </p>
              </div>

              {resetMutation.isSuccess ? (
                <div className="alert alert-success" role="alert">
                  <i className="fas fa-check-circle ms-2"></i>
                  <strong>تم إرسال البريد الإلكتروني!</strong>
                  <p className="mb-0 mt-2">
                    إذا كان البريد الإلكتروني مسجلاً في النظام، ستتلقى رسالة تحتوي على تعليمات استعادة كلمة المرور.
                  </p>
                </div>
              ) : (
                <>
                  {resetMutation.isError && (
                    <div className="alert alert-danger" role="alert">
                      <i className="fas fa-exclamation-circle ms-2"></i>
                      حدث خطأ أثناء إرسال البريد. يرجى المحاولة مرة أخرى.
                    </div>
                  )}
                  
                  <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                      <label htmlFor="email" className="form-label">
                        <i className="fas fa-envelope ms-2"></i>
                        البريد الإلكتروني
                      </label>
                      <input
                        type="email"
                        className="form-control form-control-lg"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="أدخل بريدك الإلكتروني"
                        required
                        disabled={resetMutation.isPending}
                        autoFocus
                      />
                    </div>

                    <div className="d-grid mb-3">
                      <button
                        type="submit"
                        className="btn btn-primary btn-lg"
                        disabled={resetMutation.isPending}
                      >
                        {resetMutation.isPending ? (
                          <>
                            <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>
                            جارِ الإرسال...
                          </>
                        ) : (
                          <>
                            <i className="fas fa-paper-plane ms-2"></i>
                            إرسال رابط الاستعادة
                          </>
                        )}
                      </button>
                    </div>
                  </form>
                </>
              )}

              <div className="text-center mt-4">
                <Link to="/login" className="text-decoration-none">
                  <i className="fas fa-arrow-right ms-2"></i>
                  العودة إلى تسجيل الدخول
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PasswordReset;
