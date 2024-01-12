# Dataset configuration
dataset = {
    "path": "./data",
    "path_raw": "raw",
    "path_processed": "processed",
    "path_fastdup": "fastdup",
    "path_training": "train",
    "path_test": "test",
    "classes": ["macarrones", "pizza", "tiramisu"],
    "classes_keywords": {
        "macarrones": [
            "macarrones",
            "macarrones con queso",
            "macarrones con atun",
            "macarrones con carne",
            "macarrones con pollo",
            "macarrones con salchichas",
            "macarrones con tomate",
            "macarrones con camarones",
            "macarrones con lentejas",
            "macarrones veganos",
            "macarrones vegetarianos",
            "macarrones con verduras",
            "macarrones con queso kraft",
            "macarrones hervidos",
            "macarrones integrales",
            "macarrones al pesto",
            "macarrones con gambas",
            "macaroni",
            "macaroni and cheese",
            "macaroni and tuna",
            "macaroni and meat",
            "macaroni and chiken",
            "macaroni and sausage",
            "macaroni and tomatoes",
            "macaroni and tomatoes old fashioned",
        ],
        "pizza": [
            "pizza",
            "pizza hawaiana",
            "pizza con piña",
            "pizza con peperoni",
            "pizza con queso",
            "pizza con champiñones",
            "pizza con kiwi",
            "pizza carbonara",
            "pizza de jamon y queso",
            "pizza cuatro quesos",
            "pizza barbacoa",
            "pizza pulled pork",
            "pizza margarita",
            "pizza marinera",
            "pizza vegetariana",
            "pizza capricciosa",
            "pizza napolitana",
            "pizza de trufa",
            "pizza siciliana",
            "pizza de prosciutto",
            "pizza española",
            "pizza mexicana",
            "pizza de cajun",
            "pizza de albondigas"
        ],
        "tiramisu": [
            "tiramisu",
            "tiramisu en copa",
            "tiramisu casero",
            "tiramisu de fresa",
            "tiramisu italiano",
            "tiramisu en vaso",
            "tiramisu classico",
            "tiramisu receta facil",
            "tiramisu receta",
            "tiramisu sin huevo",
            "tiramisu thermomix",
            "tiramisu de chocolate",
            "tiramisu de frutos rojos",
            "tiramisu de frutas",
            "tiramisu de maracuya",
            "tiramisu recette",
            "tiramisu mousse",
            "pastel de tiramisu",
            "bizcocho de tiramisu",
            "tarta de tiramisu",
            "tiramisu mascarpone",
            "tiramisu mascarpone cheesecake",
            "tiramisu mercadona",
            "foto tiramisu"
        ]
    },
    "classes_num_images": 1500,
    "classes_images_extension": "jpg",
    "classes_images_split_ratio": 0.95,
    "fastdup": {
        "export": True,
    }
}

# Model configuration
model = {
    "path": "./data",
    "path_models": "models",
    "path_classes": "./data/processed",
    "name": "svc_model.joblib"
}
