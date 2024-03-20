def scale_tempo(user_input):
    if user_input is None:
        return -1
    
    min_tempo = 0.0
    max_tempo = 239.44000244140625
    range_diff = max_tempo - min_tempo

    return range_diff * user_input / 10 + min_tempo

def scale_danceability(user_input):
    if user_input is None:
        return -1
    
    min_danceability = 0.0
    max_danceability = 0.9829999804496765
    range_diff = max_danceability - min_danceability

    return range_diff * user_input / 10 + min_danceability

def scale_energy(user_input):
    if user_input is None:
        return -1
    
    min_energy = 0.00017499999376013875
    max_energy = 1.0
    range_diff = max_energy - min_energy

    return range_diff * user_input / 10 + min_energy

def scale_loudness(user_input):
    if user_input is None:
        return -1
    
    min_loudness = -46.448001861572266
    max_loudness = 1.274999976158142
    range_diff = max_loudness - min_loudness

    return range_diff * user_input / 10 + min_loudness

def scale_liveness(user_input):
    if user_input is None:
        return -1
    
    min_liveness = 0.0
    max_liveness = 0.9959999918937683
    range_diff = max_liveness - min_liveness

    return range_diff * user_input / 10 + min_liveness

def scale_valence(user_input):
    if user_input is None:
        return -1
    
    min_valence = 0.0
    max_valence = 0.9909999966621399
    range_diff = max_valence - min_valence

    return range_diff * user_input / 10 + min_valence
