// This illustration keeps its state in the page only; nothing is stored or sent.
const demo = document.querySelector('[data-checklist-demo]');
if (demo) {
  const boxes = [...demo.querySelectorAll('input[type="checkbox"]')];
  const count = demo.querySelector('[data-completed-count]');
  const progress = demo.querySelector('progress');
  const update = () => {
    const completed = boxes.filter(box => box.checked).length;
    count.textContent = `${completed} / ${boxes.length}`;
    progress.value = completed;
  };
  boxes.forEach(box => box.addEventListener('change', update));
  update();
}
