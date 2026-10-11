\version "2.24.3"
%% Fichier produit par outils/generer_lecture.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new Staff {
    \clef treble
    \omit Staff.TimeSignature
    \cadenzaOn
    c'1 d'1 e'1 f'1 g'1 a'1 b'1 c''1 d''1 e''1 f''1 g''1 a''1 b''1 c'''1
    \bar "|."
  }
  \addlyrics { do ré mi fa sol la si do ré mi fa sol la si do }
  \layout { }
}
