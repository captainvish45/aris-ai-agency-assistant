class ArisChatbot {
    constructor() {
        this.steps = [];
        this.currentStep = 0;
        this.answers = {};
        this.isConfirming = false;
        this.isSubmitting = false;

        this.messagesEl = document.getElementById('chat-messages');
        this.inputArea = document.getElementById('chat-input-area');
        this.inputWrapper = document.getElementById('input-wrapper');
        this.chatForm = document.getElementById('chat-form');
        this.chatInput = document.getElementById('chat-input');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.progressFill = document.getElementById('progress-fill');
        this.progressText = document.getElementById('progress-text');
        this.summaryEl = document.getElementById('chat-summary');
        this.summaryGrid = document.getElementById('summary-grid');
        this.confirmBtn = document.getElementById('confirm-btn');
        this.editBtn = document.getElementById('edit-btn');

        this.init();
    }

    async init() {
        try {
            const response = await fetch('/api/chat/steps');
            const data = await response.json();
            this.steps = data.steps;
            this.updateProgress();
            this.bindEvents();
        } catch (error) {
            this.addBotMessage('Sorry, something went wrong loading the chat. Please refresh the page.');
        }
    }

    bindEvents() {
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

      this.confirmBtn.addEventListener('click', () => this.submitLead());
        this.editBtn.addEventListener('click', () => this.editAnswers());
    }

    updateProgress() {
        const total = this.steps.length || 8;
        const current = Math.min(this.currentStep + 1, total);
        const percent = (current / total) * 100;
        this.progressFill.style.width = `${percent}%`;
        this.progressText.textContent = `Step ${current} of ${total}`;
    }

    showTyping() {
        this.typingIndicator.classList.remove('hidden');
        this.messagesEl.scrollTop = this.messagesEl.scrollHeight;
    }

    hideTyping() {
        this.typingIndicator.classList.add('hidden');
    }

    addBotMessage(text, isError = false) {
        const div = document.createElement('div');
        div.className = 'message bot';
        div.innerHTML = `
            <div class="message-avatar">AI</div>
            <div class="message-content${isError ? ' error' : ''}">
                <p>${this.escapeHtml(text)}</p>
            </div>
        `;
        this.messagesEl.appendChild(div);
        this.messagesEl.scrollTop = this.messagesEl.scrollHeight;
    }

    addUserMessage(text) {
        const div = document.createElement('div');
        div.className = 'message user-msg';
        div.innerHTML = `
            <div class="message-avatar">You</div>
            <div class="message-content">
                <p>${this.escapeHtml(text)}</p>
            </div>
        `;
        this.messagesEl.appendChild(div);
        this.messagesEl.scrollTop = this.messagesEl.scrollHeight;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async handleSubmit() {
        if (this.isConfirming) return;

        const step = this.steps[this.currentStep];
        if (!step) return;

        let value = '';

        if (step.type === 'select') {
            const selected = this.inputWrapper.querySelector('.service-option.selected');
            if (!selected) {
                this.addBotMessage('Please select one of the service options above.', true);
                return;
            }
            value = selected.dataset.value;
        } else {
            value = this.chatInput.value.trim();
            if (!value) return;
        }

        this.addUserMessage(value);

        try {
            const validation = await fetch('/api/chat/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key: step.key, value }),
            });
            const result = await validation.json();

            if (!result.valid) {
                this.showTyping();
                await this.delay(600);
                this.hideTyping();
                this.addBotMessage(result.message, true);
            if (this.chatInput) {
    this.chatInput.value = '';
    this.chatInput.focus();
}
                return;
            }
        } catch (error) {
            this.addBotMessage('Validation failed. Please try again.', true);
            return;
        }

        this.answers[step.key] = value;
        
        this.currentStep++;
        this.updateProgress();

if (this.chatInput) {
    this.chatInput.value = '';
}

this.resetInputWrapper();

        if (this.currentStep >= this.steps.length) {
            this.showSummary();
        } else {
            this.showTyping();
            await this.delay(800);
            this.hideTyping();
            this.askCurrentQuestion();
        }
    }

    resetInputWrapper() {
        this.inputWrapper.innerHTML = `
            <input type="text" id="chat-input" placeholder="Type your answer..." autocomplete="off" required>
        `;
        this.chatInput = document.getElementById('chat-input');
    }

    askCurrentQuestion() {
        const step = this.steps[this.currentStep];
        this.addBotMessage(step.question);

        if (step.type === 'select') {
            this.renderServiceOptions(step.options);
            return;
        } else {
            this.resetInputWrapper();
            this.chatInput.focus();
            if (step.type === 'email') {
                this.chatInput.type = 'email';
                this.chatInput.placeholder = 'Enter your email address...';
            } else if (step.type === 'tel') {
                this.chatInput.type = 'tel';
                this.chatInput.placeholder = 'Enter your phone number...';
            }
        }
    }

    renderServiceOptions(options) {
        const container = document.createElement('div');
        container.className = 'service-options';

        options.forEach((option) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'service-option';
            btn.dataset.value = option;
            btn.textContent = option;
            btn.addEventListener('click', () => {
                container.querySelectorAll('.service-option').forEach((el) => {
                    el.classList.remove('selected');
                });
                btn.classList.add('selected');
            });
            container.appendChild(btn);
        });

        this.inputWrapper.innerHTML = '';
        this.inputWrapper.appendChild(container);
    }

    showSummary() {
        this.isConfirming = true;
        this.inputArea.classList.add('hidden');

        this.showTyping();
        setTimeout(async () => {
            this.hideTyping();
            this.addBotMessage("Here's a summary of your information. Please review and confirm:");

            this.summaryGrid.innerHTML = this.steps
                .map((step) => {
                    const value = this.answers[step.key] || 'N/A';
                    return `
                        <div class="summary-item">
                            <label>${step.field}</label>
                            <span>${this.escapeHtml(value)}</span>
                        </div>
                    `;
                })
                .join('');

            this.summaryEl.classList.remove('hidden');
        }, 800);
    }

    editAnswers() {
        this.isConfirming = false;
        this.currentStep = 0;
        this.answers = {};
        this.summaryEl.classList.add('hidden');
        this.inputArea.classList.remove('hidden');
        this.messagesEl.innerHTML = '';
        this.updateProgress();
        this.resetInputWrapper();
        this.addBotMessage(this.steps[0].question);
        this.chatInput.focus();
    }

    async submitLead() {
        if (this.isSubmitting) return;
        this.isSubmitting = true;

        const btnText = this.confirmBtn.querySelector('.btn-text');
        const btnLoader = this.confirmBtn.querySelector('.btn-loader');
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');
        this.confirmBtn.disabled = true;

        try {
            const response = await fetch('/api/chat/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.answers),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Submission failed');
            }

            const lead = await response.json();
            window.location.href = `/success?lead_id=${lead.id}`;
        } catch (error) {
            this.isSubmitting = false;
            btnText.classList.remove('hidden');
            btnLoader.classList.add('hidden');
            this.confirmBtn.disabled = false;
            showToast(error.message || 'Failed to submit. Please try again.', 'error');
        }
    }

    delay(ms) {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('chat-messages')) {
        new ArisChatbot();
    }
});
