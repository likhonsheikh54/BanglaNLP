// Animate statistics numbers
const animateNumbers = () => {
    document.querySelectorAll('.stat-card[data-animate="true"]').forEach(card => {
        const numberEl = card.querySelector('.stat-number');
        const targetValue = parseInt(numberEl.dataset.value);
        
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    let currentValue = 0;
                    const duration = 2000;
                    const increment = targetValue / (duration / 16);
                    
                    const animate = () => {
                        currentValue += increment;
                        if (currentValue < targetValue) {
                            numberEl.textContent = Math.round(currentValue).toLocaleString();
                            requestAnimationFrame(animate);
                        } else {
                            numberEl.textContent = targetValue.toLocaleString();
                        }
                    };
                    
                    requestAnimationFrame(animate);
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(card);
    });
};

document.addEventListener('DOMContentLoaded', () => {
    animateNumbers();
});
