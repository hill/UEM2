const palettes = [
  ["0d3b66", "faf0ca", "f4d35e", "ee964b", "f95738"],
  ["212738", "f97068", "d1d646", "edf2ef", "57c4e5"],
  ["eac435", "345995", "e40066", "03cea4", "fb4d3d"],
  ["ef476f", "ffd166", "06d6a0", "118ab2", "073b4c"],
  ["0d0630", "18314f", "384e77", "8bbeb2", "e6f9af"],
  ["483d3f", "058ed9", "f4ebd9", "a39a92", "77685d"],
];

function chooseRandomFromArray(array) {
  return array[Math.floor(Math.random() * array.length)];
}

export const PaletteService = {
  chooseRandomPalette() {
    return chooseRandomFromArray(palettes);
  },
  chooseRandomColor() {
    const palette = this.chooseRandomPalette();
    return "#" + chooseRandomFromArray(palette);
  },
  getContrastYIQ(hexcolor) {
    // see https://www.w3.org/TR/AERT/#color-contrast
    hexcolor = hexcolor.replace("#", "");
    const r = parseInt(hexcolor.substr(0, 2), 16);
    const g = parseInt(hexcolor.substr(2, 2), 16);
    const b = parseInt(hexcolor.substr(4, 2), 16);
    const yiq = (r * 299 + g * 587 + b * 114) / 1000;
    return yiq >= 128 ? "black" : "white";
  },
};
