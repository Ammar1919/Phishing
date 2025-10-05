def display_results(results):
    for result in results:
        print(f"Prediction: {result['prediction']}")
        if result['confidence']:
            print(f"Confidence: {result['confidence']:.2%}")
