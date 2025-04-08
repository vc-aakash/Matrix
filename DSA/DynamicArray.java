class DynamicArray {
    int[] array;

    public DynamicArray(int capacity) {
        this.array = new int[capacity];
    }

    public int get(int i) {
        return this.array[i];
    }

    public void set(int i, int n) {
        this.array[i] = n;
    }

//    public void pushback(int n) {
//        for (int i=0; i<this.array.length; i++) {
//            if (this.array[i] = null);
//        }
//        this.array[this.array.length] = n;
//    }
//
//    public int popback() {
//
//    }
//
//    private void resize() {
//
//    }
//
//    public int getSize() {
//
//    }
//
//    public int getCapacity() {
//
//    }
}
