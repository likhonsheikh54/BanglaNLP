document.addEventListener('DOMContentLoaded', () => {
    // Initialize copy buttons for code blocks
    document.querySelectorAll('pre code').forEach((block) => {
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.innerHTML = 'Copy';
        block.parentElement.appendChild(button);
        
        button.addEventListener('click', () => {
            navigator.clipboard.writeText(block.textContent);
            button.innerHTML = 'Copied!';
            setTimeout(() => button.innerHTML = 'Copy', 2000);
        });
    });

    // Add animation to feature cards
    const cards = document.querySelectorAll('.feature-card');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    cards.forEach(card => observer.observe(card));
});
