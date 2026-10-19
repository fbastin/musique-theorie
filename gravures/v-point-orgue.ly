\version "2.24.3"
%% Fichier produit par outils/generer_valeurs.py — ne pas modifier à la main.
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
  \new Staff  {
      \clef treble \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      \textMark \markup \small \italic "sur une note" c''4 b'4 c''2\fermata \bar "|" \textMark \markup \small \italic "sur un silence" e''4 r4\fermata d''2
      \bar "|."
    }
  \layout {
     line-width = 300\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \markLengthOn \override TextMark.self-alignment-X = #LEFT }
  }
}
