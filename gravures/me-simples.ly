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
        \time 2/4 c''4 d''4 | \time 3/4 c''4 d''4 e''4 | \time 4/4 c''4 d''4 e''4 f''4 | \time 2/2 c''2 d''2 | \time 3/8 c''8[ d''8 e''8]
        \bar "|."
      }
      \new NullVoice = "temps" { b'4 b'4 b'4 b'4 b'4 b'4 b'4 b'4 b'4 b'2 b'2 b'8 b'8 b'8 }
    >>
    \new Lyrics \with { \override LyricText.font-size = #-1 } \lyricsto "temps" { "1" "2" "1" "2" "3" "1" "2" "3" "4" "1" "2" "1" "2" "3" }
  >>
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
