// ============================================
// Main Frontend Scripts
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // Confirm password validation on register page
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password');
            const confirm = document.getElementById('confirm_password');
            
            if (password && confirm && password.value !== confirm.value) {
                e.preventDefault();
                alert('Passwords do not match!');
            }
        });
    }

    // Add smooth focus effects
    const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], input[type="number"]');
    inputs.forEach(function(input) {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
});

// ============================================
// Tab Switch for Login Page
// ============================================
function switchTab(tab) {
    const loginTypeInput = document.getElementById('login_type');
    if (loginTypeInput) {
        loginTypeInput.value = tab;
    }

    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(function(btn) {
        btn.classList.remove('active');
    });

    const activeBtn = document.querySelector('.tab-btn[data-tab="' + tab + '"]');
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
}
