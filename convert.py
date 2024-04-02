import os
import json

from PIL import Image  # type: ignore
from dotenv import load_dotenv

from apryse_sdk import (  # type: ignore
    PDFNet,
    PDFDoc,
    Convert,
    SDFDoc,
    FDFDoc,
    ConversionOptions,
    DocumentConversion,
)

load_dotenv()

PDFNet.Initialize(os.getenv("LICENSE"))


def create_pdf_with_annotations(
    image_path: str = "static/test_img.jpeg",
    save_as: str = "output.pdf",
    annotations_path: str = "test_annotation.xml",
    use_streaming: bool = True,
):
    """Convert an image to a PDF and merge it with annotations."""
    pdf = PDFDoc()
    if use_streaming:
        pdf = convert_to_pdf_streaming(pdf, image_path)
    else:
        Convert.ToPdf(pdf, image_path)

    fdfDoc = FDFDoc.CreateFromXFDF(annotations_path)
    pdf.FDFMerge(fdfDoc)

    pdf.Save(save_as, SDFDoc.e_remove_unused)


def convert_to_pdf_streaming(pdf: PDFDoc, image_path: str) -> PDFDoc:
    width, height, dpi = get_image_info(image_path)
    print(f"Image size: {width}x{height} at {dpi} DPI")

    options: dict = {
        "DPI": dpi,
        # "RemovePadding": True,
        # "PageSizes": [width, height],
        # "DefaultPageSize": [width, height],
    }
    print(f"Conversion options: {options}")

    conversion_options = ConversionOptions(json.dumps(options))
    converter = Convert.StreamingPDFConversion(
        pdf, image_path, conversion_options
    )  # noqa

    while converter.GetConversionStatus() == DocumentConversion.eIncomplete:
        converter.TryConvert()
        if converter.GetConversionStatus() == DocumentConversion.eSuccess:
            return pdf
        else:
            print("Conversion failed")
            print(converter.GetErrorString())

    return pdf


def get_image_info(image_path: str) -> tuple[int, int, int]:
    """
    Get the width, height and dpi of an image.
    If the dpi is not set, it will default to 72.
    """
    with Image.open(image_path) as img:
        width, height = img.size
        dpi = img.info.get("dpi", (72, 72))[0]
        return width, height, dpi


if __name__ == "__main__":
    create_pdf_with_annotations()
