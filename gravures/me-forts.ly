\version "2.24.3"
%% Fichier produit par outils/generer_mesure.py — ne pas modifier à la main.
\paper {
  indent = 0
  paper-width = 152\mm
  line-width = 150\mm
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
  <<
    \new Staff <<
      \new Voice {
        \clef treble \autoBeamOff \numericTimeSignature
        \time 2/4 c''4 d''4 | \time 3/4 c''4 d''4 e''4 | \time 4/4 c''4 d''4 e''4 f''4
        \bar "|."
      }
      \new NullVoice = "temps" { b'4 b'4 b'4 b'4 b'4 b'4 b'4 b'4 b'4 }
    >>
    \new Lyrics \with { \override LyricText.font-size = #-1 \override LyricText.font-shape = #'italic \override LyricSpace.minimum-distance = #1.5 } \lyricsto "temps" { "fort" "faible" "fort" "faible" "faible" "fort" "faible" "mi-fort" "faible" }
  >>
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
