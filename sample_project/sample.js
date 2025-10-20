// Utility math functions
function add(a, b) {
  return a + b;
}

class Calculator {
  constructor() {
    this.total = 0;
  }
  add(x) {
    this.total += x;
    return this.total;
  }
}
