export interface Image {
  src: string;
  alt: string;
}

export interface LexicaImage extends Image {
  prompt: string;
  dimensions: string;
}

export interface Style {
  style_name: string;
  style_link: string;
  images: Image[];
  lexica_images: LexicaImage[];
  keywords: string[];
}

export interface StylesData {
  styles: Style[];
}