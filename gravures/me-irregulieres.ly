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
  \new Staff { \new Voice {
        \clef treble \autoBeamOff \numericTimeSignature
        \time 5/4 c''4->^\markup \small \italic "3 + 2" d''4 e''4 f''4-> g''4 | \time 7/8 c''8[->^\markup \small \italic "2 + 2 + 3" d''8] e''8[-> f''8] g''8[-> f''8 e''8] | c''8[->^\markup \small \italic "3 + 2 + 2" d''8 e''8] f''8[-> e''8] d''8[-> c''8]
        \bar "|."
      } }
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
