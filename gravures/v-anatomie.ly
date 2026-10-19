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
      \textMark \markup \small \italic "hampe montante" a'8 \bar "|" \textMark \markup \small \italic "hampe descendante" e''8 \bar "|" \textMark \markup \small \italic "ligature" a'8[ c''8]
      \bar "|."
    }
  \layout {
     line-width = 300\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #2.4 \markLengthOn \override TextMark.self-alignment-X = #LEFT }
  }
}
