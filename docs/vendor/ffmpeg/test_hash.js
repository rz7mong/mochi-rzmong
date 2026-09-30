class T { #e = 1; test() { return this.#e; } }
console.log(new T().test());
